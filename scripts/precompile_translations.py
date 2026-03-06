#!/usr/bin/env python3
"""
Pre-compile FTL translation files to Python bytecode for fast startup.

This script is run during Docker image build to avoid the slow compile_messages()
call (44s on Alpine musl) at container startup. Instead, startup loads .pyc files
in ~50ms total.

Usage:
    python3 scripts/precompile_translations.py <translations_dir> <output_dir>

Output:
    <output_dir>/ftl_<locale>.py  -- Python source with compiled message functions
    <output_dir>/__pycache__/ftl_<locale>.cpython-312.pyc  -- Python bytecode
"""

import ast
import pathlib
import py_compile
import sys
import time

from fluent_compiler.compiler import compile_messages
from fluent_compiler.resource import FtlResource


def precompile(translations_dir: pathlib.Path, output_dir: pathlib.Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    locales = sorted(p.name for p in translations_dir.iterdir() if p.is_dir())
    if not locales:
        print(f"ERROR: No locale directories found in {translations_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Pre-compiling translations for locales: {locales}")
    t_total = time.time()

    for locale in locales:
        t0 = time.time()
        ftl_dir = translations_dir / locale
        files = sorted(ftl_dir.rglob("*.ftl"))

        if not files:
            print(f"  {locale}: WARNING - no .ftl files found, skipping")
            continue

        text = "\n".join(f.read_text(encoding="utf-8") for f in files)

        result = compile_messages(locale, [FtlResource(text)], use_isolating=False)

        if result.errors:
            for msg_id, err in result.errors:
                print(f"  {locale}: WARNING - compilation error in '{msg_id}': {err}")

        # Convert AST to Python source
        py_source = ast.unparse(result.module_ast)

        # Append message_id -> function_name mapping so startup can restore
        # _compiled_messages dict without calling compile_messages() again
        keys_map = {k: v.__name__ for k, v in result.message_functions.items()}
        py_source += "\n\n__message_keys__ = " + repr(keys_map) + "\n"

        out_file = output_dir / f"ftl_{locale}.py"
        out_file.write_text(py_source, encoding="utf-8")

        # Compile to .pyc bytecode (stored in __pycache__ alongside .py)
        pyc_path = py_compile.compile(str(out_file), doraise=True)

        elapsed = time.time() - t0
        print(
            f"  {locale}: {len(result.message_functions)} messages, "
            f"{len(py_source):,} chars -> {pyc_path} ({elapsed:.1f}s)"
        )

    print(f"Done in {time.time() - t_total:.1f}s")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <translations_dir> <output_dir>")
        sys.exit(1)

    translations_dir = pathlib.Path(sys.argv[1])
    output_dir = pathlib.Path(sys.argv[2])

    if not translations_dir.exists():
        print(f"ERROR: translations_dir does not exist: {translations_dir}", file=sys.stderr)
        sys.exit(1)

    precompile(translations_dir, output_dir)
