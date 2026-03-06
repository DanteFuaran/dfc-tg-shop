"""
PrecompiledStorage: loads FluentBundle from pre-compiled Python bytecode (.pyc).

This replaces FileStorage during Docker image build:
  - Docker build step runs precompile_translations.py → generates ftl_{locale}.py + .pyc
  - At container startup, this storage loads .pyc files (12-15ms per locale) instead
    of calling FluentBundle.from_string() which takes 11s per locale on Alpine musl.

Total startup saving: ~44s → ~150ms (300x faster).
"""

from __future__ import annotations

import builtins
import importlib.util
import pathlib
import types
from typing import TYPE_CHECKING

import babel
from fluent_compiler.bundle import FluentBundle
from fluent_compiler.compiler import BUILTINS as FLUENT_BUILTINS
from fluent_compiler.compiler import _parse_resources, messages_to_module
from fluent_compiler.resource import FtlResource
from fluentogram import FluentTranslator
from fluentogram.storage.base import BaseStorage
from loguru import logger

if TYPE_CHECKING:
    pass

# Names that are available as Python builtins — no need to inject them
_PYTHON_BUILTINS: frozenset[str] = frozenset(dir(builtins))

# Minimal placeholder FTL to bootstrap module_globals without compiling real FTL
_PLACEHOLDER_FTL = "_placeholder = x"


def _make_runtime_globals(locale_code: str) -> dict:
    """
    Build the runtime globals dict that fluent_compiler injects into compiled modules.

    This includes: handle_argument, handle_output, FluentNone, FluentReferenceError,
    plural_form_for_number, NUMBER, DATETIME, locale (babel.Locale), etc.

    We use a minimal placeholder FTL to call messages_to_module() which builds
    these globals cheaply (~1ms) without compiling any real translations.
    """
    babel_locale = babel.Locale.parse(locale_code.replace("-", "_"))
    messages, _ = _parse_resources([FtlResource(_PLACEHOLDER_FTL)])
    _, _, module_globals, _ = messages_to_module(
        messages,
        babel_locale,
        use_isolating=False,
        functions=FLUENT_BUILTINS.copy(),
    )
    return module_globals


class PrecompiledStorage(BaseStorage):
    """
    Storage that loads FluentBundle message functions from pre-compiled .pyc files
    instead of re-compiling FTL source on every container start.

    Expected directory layout (created by scripts/precompile_translations.py):

        precompiled_dir/
            ftl_ru.py
            ftl_uk.py
            ftl_en.py
            ftl_de.py
            __pycache__/
                ftl_ru.cpython-312.pyc   ← loaded in ~12ms instead of ~11s
                ftl_uk.cpython-312.pyc
                ...
    """

    def __init__(self, precompiled_dir: pathlib.Path) -> None:
        super().__init__()
        self._precompiled_dir = precompiled_dir
        self._load_precompiled()

    def _load_precompiled(self) -> None:
        py_files = sorted(self._precompiled_dir.glob("ftl_*.py"))

        if not py_files:
            raise FileNotFoundError(
                f"No precompiled translation files found in {self._precompiled_dir}. "
                "Run scripts/precompile_translations.py during Docker build."
            )

        for py_file in py_files:
            locale = py_file.stem.removeprefix("ftl_")
            logger.debug(f"Loading precompiled translations for locale: {locale}")

            # Build the runtime globals dict for this locale (~1ms each)
            runtime_globals = _make_runtime_globals(locale)
            runtime_keys = [
                k for k in runtime_globals
                if not k.startswith("__") and k not in _PYTHON_BUILTINS
            ]

            # importlib automatically uses __pycache__/<name>.cpython-312.pyc
            # if it exists and is up-to-date — that's where the speed comes from
            spec = importlib.util.spec_from_file_location(f"ftl_{locale}", str(py_file))
            if spec is None or spec.loader is None:
                raise ImportError(f"Cannot load precompiled module for locale {locale}: {py_file}")

            mod: types.ModuleType = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)  # type: ignore[union-attr]

            if not hasattr(mod, "__message_keys__"):
                raise AttributeError(
                    f"Precompiled module for locale {locale} is missing __message_keys__. "
                    "Re-run scripts/precompile_translations.py."
                )

            # Inject runtime globals into the module so compiled message functions
            # can resolve handle_argument, FluentNone, locale, etc.
            # Python functions look up names through __globals__ (== mod.__dict__),
            # so injecting into the module dict makes them available at call time.
            for key in runtime_keys:
                setattr(mod, key, runtime_globals[key])

            # Restore {message_id: callable} mapping that FluentBundle._compiled_messages expects
            message_functions: dict[str, types.FunctionType] = {
                msg_id: getattr(mod, func_name)
                for msg_id, func_name in mod.__message_keys__.items()
            }

            # Build a FluentBundle without calling compile_messages() (which would be slow)
            bundle: FluentBundle = object.__new__(FluentBundle)
            bundle.locale = locale
            bundle._compiled_messages = message_functions
            bundle._compilation_errors = []

            self.add_translator(FluentTranslator(locale=locale, translator=bundle))
            logger.debug(
                f"Loaded {locale}: {len(message_functions)} messages from precompiled .pyc"
            )

    async def close(self) -> None:
        pass
