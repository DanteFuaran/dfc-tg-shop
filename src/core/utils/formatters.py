from __future__ import annotations

from typing import TYPE_CHECKING, Final, Optional, Union

if TYPE_CHECKING:
    from src.infrastructure.database.models.dto import UserDto

import html
import re
import unicodedata
from calendar import monthrange
from datetime import datetime, timedelta
from decimal import ROUND_HALF_UP, ROUND_UP, Decimal
from re import Match
from urllib.parse import quote

from src.core.constants import T_ME
from src.core.enums import Currency, PlanType
from src.core.i18n.keys import ByteUnitKey, TimeUnitKey, UtilKey
from src.core.utils.time import datetime_now

_HTML_RE = re.compile(r"<[^>]*>")
_URL_RE = re.compile(r"(?i)\b(?:https?://|www\.|tg://|t\.me/|telegram\.me/|joinchat/)\S+")
_USER_NAME_PLACEHOLDER = "User123"


# For only user action
def format_user_log(user: Union["BaseUserDto", "UserDto"]) -> str:  # noqa: F821
    return f"[{user.role.upper()}:{user.telegram_id} ({user.name})]"


def format_user_name(name: Optional[str]) -> str:
    if not name:
        return _USER_NAME_PLACEHOLDER

    text = html.unescape(name)
    text = unicodedata.normalize("NFKC", text)

    text = _HTML_RE.sub("", text)
    text = _URL_RE.sub("", text)

    allowed_prefixes = {"L", "N"}
    allowed_symbols = {"$", "_", "-", "."}

    chars: list[str] = []

    for char in text:
        cat = unicodedata.category(char)

        if cat == "Mn":
            continue

        if cat[0] in allowed_prefixes or char in allowed_symbols or cat == "Zs":
            chars.append(char)

    cleaned = " ".join("".join(chars).split())

    if not cleaned:
        return _USER_NAME_PLACEHOLDER

    if len(cleaned) > 32:
        cleaned = f"{cleaned[:31]}"

    return cleaned


def format_username_to_url(username: str, text: Optional[str]) -> str:
    clean_username = username.lstrip("@")
    # Numeric ID — use tg://user?id=... (t.me doesn't work for user IDs)
    if clean_username.lstrip("-").isdigit():
        return f"tg://user?id={clean_username}"
    encoded_text = quote(text or "")
    return f"{T_ME}{clean_username}?text={encoded_text}"


def format_days_to_datetime(value: int, year: int = 2099) -> datetime:
    dt = datetime_now()

    if value == -1:  # UNLIMITED for panel
        try:
            return dt.replace(year=year)
        except ValueError:
            last_day = monthrange(year, dt.month)[1]
            return dt.replace(year=year, day=min(dt.day, last_day))

    # Проверяем, не превышает ли значение максимально допустимое для timedelta
    # Максимум ~2,9 млн дней (datetime.max - datetime.min)
    # Если значение слишком большое (например, 999999), считаем его безлимитным
    MAX_SAFE_DAYS = 365 * 500  # ~500 лет - разумный максимум
    if value > MAX_SAFE_DAYS:
        try:
            return dt.replace(year=year)
        except ValueError:
            last_day = monthrange(year, dt.month)[1]
            return dt.replace(year=year, day=min(dt.day, last_day))
    
    try:
        return dt + timedelta(days=value)
    except OverflowError:
        # Если все еще overflow, возвращаем максимальную дату
        try:
            return dt.replace(year=year)
        except ValueError:
            last_day = monthrange(year, dt.month)[1]
            return dt.replace(year=year, day=min(dt.day, last_day))


def format_device_count(value: Optional[int]) -> int:
    if value == 0 or value is None:
        return -1  # UNLIMITED for bot

    if value == -1:
        return 0  # UNLIMITED for panel

    return value


def format_gb_to_bytes(value: int, *, binary: bool = True) -> int:
    gb_value = Decimal(value)

    if gb_value == -1:
        return 0  # UNLIMITED for panel

    multiplier = Decimal(1024**3) if binary else Decimal(10**9)
    bytes_value = (gb_value * multiplier).quantize(Decimal("1"), rounding=ROUND_HALF_UP)

    return max(0, int(bytes_value))


def format_bytes_to_gb(value: Optional[int], *, binary: bool = True) -> int:
    if not value or value == 0:
        return -1  # UNLIMITED for bot

    bytes_value = Decimal(value)

    multiplier = Decimal(1024**3) if binary else Decimal(10**9)
    gb_value = (bytes_value / multiplier).quantize(Decimal("1"), rounding=ROUND_HALF_UP)

    return max(0, int(gb_value))


def format_limits_to_plan_type(traffic: int, devices: int) -> PlanType:
    has_traffic = traffic > 0
    has_devices = devices > 0

    if has_traffic and has_devices:
        return PlanType.BOTH
    elif has_traffic:
        return PlanType.TRAFFIC
    elif has_devices:
        return PlanType.DEVICES
    else:
        return PlanType.UNLIMITED


def format_percent(part: int, whole: int) -> str:
    if whole == 0:
        return "N/A"

    percent = (part / whole) * 100
    return f"{percent:.2f}"


def format_country_code(code: str) -> str:
    if not code or not code.isalpha() or len(code) != 2:
        return "🏴‍☠️"

    return "".join(chr(ord("🇦") + ord(c.upper()) - ord("A")) for c in code)


def i18n_format_bytes_to_unit(
    value: Optional[Union[int, float]],
    *,
    round_up: bool = False,
    min_unit: ByteUnitKey = ByteUnitKey.GIGABYTE,
) -> tuple[str, dict[str, float]]:
    if value == -1:
        return UtilKey.UNLIMITED, {}

    if not value:
        value = 0

    bytes_value = Decimal(value)
    units: Final[list[ByteUnitKey]] = list(ByteUnitKey)  # [B, KB, MB, GB]

    for i, unit in enumerate(units):
        if i + 1 < len(units):
            next_unit_threshold = Decimal(1024)
            if bytes_value >= next_unit_threshold:
                bytes_value /= Decimal(1024)
            else:
                break

    if units.index(unit) < units.index(min_unit):
        unit = min_unit
        factor = Decimal(1024) ** (units.index(min_unit))
        bytes_value = Decimal(value) / factor

    rounding = ROUND_UP if round_up else ROUND_HALF_UP
    size_formatted = bytes_value.quantize(Decimal("0.01"), rounding=rounding)

    return unit, {"value": float(size_formatted)}


def i18n_format_seconds(
    value: Union[int, float, str],
) -> list[tuple[str, dict[str, int]]]:
    remaining = int(value)
    parts = []

    if remaining < 60:
        return [(TimeUnitKey.MINUTE, {"value": 0})]

    units: dict[str, int] = {
        TimeUnitKey.DAY: 86400,
        TimeUnitKey.HOUR: 3600,
        TimeUnitKey.MINUTE: 60,
    }

    for unit, unit_seconds in units.items():
        value = remaining // unit_seconds
        if value > 0:
            parts.append((unit, {"value": value}))
            remaining %= unit_seconds

    if not parts:
        return [(TimeUnitKey.MINUTE, {"value": 1})]

    return parts


def pluralize_days(count: int) -> str:
    """Returns the plural form key for days.
    
    Note: This function returns i18n keys instead of hardcoded Russian strings.
    The actual translation should be done via i18n.get() with proper pluralization.
    """
    # Return the key for unit-day which handles pluralization in FTL files
    return "unit-day"


def i18n_format_days(value: int) -> tuple[str, dict[str, int]]:
    if value is None or value == -1:  # UNLIMITED
        return UtilKey.UNLIMITED, {}

    if value % 365 == 0:
        return TimeUnitKey.YEAR, {"value": value // 365}

    if value % 30 == 0:
        return TimeUnitKey.MONTH, {"value": value // 30}

    return TimeUnitKey.DAY, {"value": value}


def i18n_format_limit(value: Optional[int]) -> tuple[str, dict[str, int]]:
    if value is None:
        return UtilKey.UNLIMITED, {}
    return UtilKey.UNIT_UNLIMITED, {"value": value}


def i18n_format_traffic_limit(value: int) -> tuple[str, dict[str, int]]:
    if value == -1:
        return UtilKey.UNIT_UNLIMITED, {"value": value}

    return ByteUnitKey.GIGABYTE, {"value": value}


def i18n_format_device_limit(value: int) -> tuple[str, dict[str, int]]:
    return UtilKey.UNIT_UNLIMITED, {"value": value}


def i18n_format_expire_time(expiry: Union[timedelta, datetime]) -> list[tuple[str, dict[str, int]]]:
    # Special case: unlimited remnawave ;D
    if isinstance(expiry, datetime) and expiry.year == 2099:
        return [(UtilKey.UNLIMITED, {"value": -1})]

    # Convert datetime to timedelta
    if isinstance(expiry, datetime):
        now = datetime_now()
        delta = expiry - now
    else:
        delta = expiry

    if delta.total_seconds() <= 0:
        # Already expired or zero
        return [("expired", {"value": 0})]

    days = delta.days
    seconds = delta.seconds
    parts: list[tuple[str, dict[str, int]]] = []

    # Years
    years, days = divmod(days, 365)
    if years:
        parts.append((TimeUnitKey.YEAR, {"value": years}))

    # Remaining days
    if days:
        parts.append((TimeUnitKey.DAY, {"value": days}))

    # Hours
    hours, seconds = divmod(seconds, 3600)
    if hours:
        parts.append((TimeUnitKey.HOUR, {"value": hours}))

    # Minutes
    minutes, _ = divmod(seconds, 60)
    if minutes:
        parts.append((TimeUnitKey.MINUTE, {"value": minutes}))

    # Default to 1 minute if everything is zero
    return parts or [("unknown", {"value": 0})]


def format_price(price: int | Decimal, currency: Currency) -> str:
    """Format price with proper decimal places based on currency type.
    
    Args:
        price: Price as integer (in base units - rubles for RUB, cents for USD/EUR) 
               or Decimal (already in target currency units)
        currency: Currency enum
        
    Returns:
        Formatted price string like "100 ₽" or "1.27 $"
    """
    if currency == Currency.RUB:
        # Rubles: price is in rubles (not kopecks)
        if isinstance(price, Decimal):
            return f"{int(price)} ₽"
        return f"{price} ₽"
    elif currency == Currency.XTR:
        # Telegram Stars: whole numbers
        if isinstance(price, Decimal):
            return f"{int(price)} {currency.symbol}"
        return f"{price} {currency.symbol}"
    else:
        # USD/EUR: handle both cents (int) and decimal amounts (Decimal)
        if isinstance(price, Decimal):
            # Already in target currency (dollars/euros)
            return f"{price:.2f} {currency.symbol}"
        else:
            # Price is in cents, convert to decimal
            decimal_price = Decimal(price) / Decimal(100)
            return f"{decimal_price:.2f} {currency.symbol}"


_VS15 = '\uFE0E'  # text variation selector — monochromatic emoji
_VS16 = '\uFE0F'  # emoji variation selector — colored emoji
_ZWJ  = '\u200D'  # zero width joiner (part of compound emoji sequences)


def make_emoji_monochrome(text: str) -> str:
    """Add VS15 (\uFE0E) after emoji to force monochromatic/text presentation.

    - Emoji followed by VS16 (\uFE0F): replace VS16 → VS15
    - Emoji already followed by VS15: skip
    - Emoji followed by ZWJ (compound sequence): skip
    - Regional indicators (flags 🇷🇺 etc.): skip
    - Otherwise: insert VS15 after the emoji
    """
    chars = list(text)
    result: list[str] = []
    i = 0
    while i < len(chars):
        c = chars[i]
        cp = ord(c)

        # Skip regional indicator pairs (flag sequences U+1F1E0..U+1F1FF)
        if 0x1F1E0 <= cp <= 0x1F1FF:
            result.append(c)
            if i + 1 < len(chars) and 0x1F1E0 <= ord(chars[i + 1]) <= 0x1F1FF:
                result.append(chars[i + 1])
                i += 2
            else:
                i += 1
            continue

        # Detect emoji codepoints
        is_emoji = (
            (0x1F000 <= cp <= 0x1FFFF)    # Supplementary: faces, objects, symbols…
            or (0x2600 <= cp <= 0x27BF)    # Misc symbols & dingbats
            or (0x2300 <= cp <= 0x23FF)    # Misc technical
            or (0x25A0 <= cp <= 0x25FF)    # Geometric shapes
            or (0x2B00 <= cp <= 0x2BFF)    # Misc symbols and arrows
            or cp in (
                0x00A9, 0x00AE,            # © ®
                0x203C, 0x2049,            # ‼ ⁉
                0x20E3,                    # combining enclosing keycap
                0x303D, 0x3030,            # 〽 〰
            )
        )

        if is_emoji:
            result.append(c)
            nxt = chars[i + 1] if i + 1 < len(chars) else ''
            if nxt == _VS15:
                # Already monochrome — keep as-is
                result.append(nxt)
                i += 2
            elif nxt == _VS16:
                # Replace colored selector with monochrome
                result.append(_VS15)
                i += 2
            elif nxt == _ZWJ:
                # Part of a compound emoji (e.g. family sequences) — don't touch
                i += 1
            else:
                result.append(_VS15)
                i += 1
        else:
            result.append(c)
            i += 1

    return ''.join(result)


def i18n_postprocess_text(text: str, collapse_level: int = 2) -> str:
    def collapse_html_tags(txt: str) -> str:
        pattern = r"<(\w+)>[\n\r]+(.*?)[\n\r]+</\1>"

        def tag_replacer(match: Match[str]) -> str:
            tag = match[1]
            content = match[2].rstrip()
            return f"<{tag}>{content}</{tag}>"

        return re.sub(pattern, tag_replacer, txt, flags=re.DOTALL)

    def normalize_newlines(txt: str) -> str:
        max_newlines = "\n" * collapse_level
        pattern = rf"(?:\n[ \t]*){{{collapse_level + 1},}}"
        return re.sub(pattern, max_newlines, txt)

    def remove_empty_markers(txt: str) -> str:
        return re.sub(r"\s*!empty!\s*", "", txt)

    text = collapse_html_tags(text)
    text = normalize_newlines(text)
    text = remove_empty_markers(text)

    return text
