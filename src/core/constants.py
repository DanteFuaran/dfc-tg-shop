import re
from datetime import timezone
from pathlib import Path
from re import Pattern
from typing import Final

BASE_DIR: Final[Path] = Path(__file__).resolve().parents[2]
ASSETS_DIR: Final[Path] = BASE_DIR / "assets"
LOG_DIR: Final[Path] = BASE_DIR / "logs"

# Ветка обновлений — единый источник: version
_update_file: Final[Path] = BASE_DIR / "version"
try:
    _update_content = _update_file.read_text()
    DEFAULT_BRANCH: Final[str] = next(
        (line.split(":", 1)[1].strip() for line in _update_content.splitlines() if line.startswith("branch:")),
        "main",
    )
except FileNotFoundError:
    DEFAULT_BRANCH: Final[str] = "main"


def get_update_branch() -> str:
    """Динамически читает ветку из version файла (перечитывает при каждом вызове).

    Это позволяет переключать ветку обновлений без перезапуска бота —
    достаточно изменить файл version.
    """
    try:
        for line in _update_file.read_text().splitlines():
            if line.startswith("branch:"):
                branch = line.split(":", 1)[1].strip()
                if branch:
                    return branch
    except (FileNotFoundError, OSError):
        pass
    return "main"

DOMAIN_REGEX: Pattern[str] = re.compile(r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$")
TAG_REGEX: Pattern[str] = re.compile(r"^[A-Z0-9_]+$")
URL_PATTERN: Pattern[str] = re.compile(r"^https?://.*$")
USERNAME_PATTERN: Pattern[str] = re.compile(r"^@[a-zA-Z0-9_]{5,32}$")
DATETIME_FORMAT: Final[str] = "%d.%m.%Y %H:%M:%S"

T_ME: Final[str] = "https://t.me/"
API_V1: Final[str] = "/api/v1"
BOT_WEBHOOK_PATH: Final[str] = "/telegram"
PAYMENTS_WEBHOOK_PATH: Final[str] = "/payments"
REMNAWAVE_WEBHOOK_PATH: Final[str] = "/remnawave"
REPOSITORY: Final[str] = "https://github.com/DanteFuaran/dfc-tg-shop"

TIMEZONE: Final[timezone] = timezone.utc
DFC_SHOP_PREFIX: Final[str] = ""
PURCHASE_PREFIX: Final[str] = "purchase_"
GOTO_PREFIX: Final[str] = "gt_"
ENCRYPTED_PREFIX: Final[str] = "enc_"
REFERRAL_PREFIX: Final[str] = "ref_"

IMPORTED_TAG: Final[str] = "IMPORTED"

MIDDLEWARE_DATA_KEY: Final[str] = "middleware_data"
CONTAINER_KEY: Final[str] = "dishka_container"
CONFIG_KEY: Final[str] = "config"
USER_KEY: Final[str] = "user"
SETTINGS_KEY: Final[str] = "settings"
IS_SUPER_DEV_KEY: Final[str] = "is_super_dev"

TIME_1M: Final[int] = 60
TIME_5M: Final[int] = TIME_1M * 5
TIME_10M: Final[int] = TIME_1M * 10

RECENT_REGISTERED_MAX_COUNT: Final[int] = 25
RECENT_ACTIVITY_MAX_COUNT: Final[int] = 25

BATCH_SIZE: Final[int] = 20
BATCH_DELAY: Final[int] = 1
