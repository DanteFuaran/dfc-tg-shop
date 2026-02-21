import os
from pathlib import Path

# Читаем версию из файла version
# Поддерживаемые форматы:
#   plain:         0.4.21
#   с префиксом:   version: 0.4.21
# Приоритет: файл version → переменная окружения BUILD_TAG → "0.0.0"
_version_file = Path(__file__).parent.parent / "version"

try:
    _raw = _version_file.read_text().strip()
    # Поддерживаем оба формата
    if _raw.startswith("version:"):
        __version__ = _raw.split(":", 1)[1].strip()
    else:
        # Plain format: берём первую непустую строку
        _first_line = next((l.strip() for l in _raw.splitlines() if l.strip()), "")
        __version__ = _first_line or os.environ.get("BUILD_TAG", "0.0.0")
except FileNotFoundError:
    __version__ = os.environ.get("BUILD_TAG", "0.0.0")
