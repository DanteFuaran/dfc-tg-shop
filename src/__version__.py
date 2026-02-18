from pathlib import Path

# Читаем версию из файла version (формат: version: x.x.x)
_update_file = Path(__file__).parent.parent / "version"

try:
    for _line in _update_file.read_text().splitlines():
        if _line.startswith("version:"):
            __version__ = _line.split(":", 1)[1].strip()
            break
    else:
        __version__ = "0.0.0"
except FileNotFoundError:
    __version__ = "0.0.0"
