from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from io import BytesIO
from typing import Any, Optional

from aiogram.types import BufferedInputFile, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedScroll
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner

from src.core.enums import PurchaseType, TransactionStatus
from src.infrastructure.database.models.dto import TransactionDto, UserDto
from src.services.transaction import TransactionService
from src.services.user import UserService

MAX_CAPTION_LEN = 1000

MONTH_NAMES = {
    1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель",
    5: "Май", 6: "Июнь", 7: "Июль", 8: "Август",
    9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь",
}

MONTH_SHORT = {
    1: "янв", 2: "фев", 3: "мар", 4: "апр",
    5: "май", 6: "июн", 7: "июл", 8: "авг",
    9: "сен", 10: "окт", 11: "ноя", 12: "дек",
}


def _format_date(dt: datetime) -> str:
    return dt.strftime("%d.%m.%Y")


def _format_time(dt: datetime) -> str:
    return dt.strftime("%H:%M")


def _user_label(user: UserDto) -> str:
    if user.username:
        return f"@{user.username}"
    return user.name


def _tg_link(tid: int | str) -> str:
    return f'<code>{tid}</code>'


def _purchase_emoji(tx: TransactionDto) -> str:
    match tx.purchase_type:
        case PurchaseType.NEW:
            return "🛒"
        case PurchaseType.RENEW:
            return "🔄"
        case PurchaseType.CHANGE:
            return "🔃"
        case PurchaseType.TOPUP:
            return "💰"
        case PurchaseType.EXTRA_DEVICES:
            return "📱"
        case _:
            return "❓"


def _payment_word(n: int) -> str:
    if 11 <= n % 100 <= 19:
        return "платежей"
    last = n % 10
    if last == 1:
        return "платеж"
    if 2 <= last <= 4:
        return "платежа"
    return "платежей"


def _user_word(n: int) -> str:
    if 11 <= n % 100 <= 19:
        return "новых пользователей"
    last = n % 10
    if last == 1:
        return "новый пользователь"
    if 2 <= last <= 4:
        return "новых пользователя"
    return "новых пользователей"


def _format_registrations(users: list[UserDto], max_len: int, *, month: int = 0, year: int = 0) -> str:
    sorted_users = sorted(
        [u for u in users if u.created_at],
        key=lambda u: u.created_at,  # type: ignore[arg-type]
        reverse=True,
    )

    if month > 0:
        sorted_users = [u for u in sorted_users if u.created_at.month == month]  # type: ignore[union-attr]
    if year > 0:
        sorted_users = [u for u in sorted_users if u.created_at.year == year]  # type: ignore[union-attr]

    if not sorted_users:
        return "Нет записей"

    total_count = len(sorted_users)
    itogo = f"\n────────────────────────────\n<b>Итого:</b> {total_count} {_user_word(total_count)}"
    effective_max = max_len - len(itogo)

    max_tid_len = max(len(str(u.telegram_id)) for u in sorted_users)

    groups: dict[str, list[UserDto]] = defaultdict(list)
    for user in sorted_users:
        groups[_format_date(user.created_at)].append(user)  # type: ignore[arg-type]

    result = ""
    for date_key, entries in groups.items():
        quote_lines = []
        for user in entries:
            time_str = _format_time(user.created_at)  # type: ignore[arg-type]
            raw_tid = str(user.telegram_id)
            missing = max_tid_len - len(raw_tid)
            pad = " " * (missing * 2)
            tid_link = pad + _tg_link(raw_tid)
            label = _user_label(user)
            quote_lines.append(f"  {time_str} | {tid_link} | {label}")

        sep = "\n\n" if result else ""
        block_header = f"{sep}📅 <b>{date_key}</b>\n<blockquote>"
        block_footer = "</blockquote>"
        remaining = effective_max - len(result) - len(block_header) - len(block_footer)
        if remaining < len(quote_lines[0]):
            break

        included: list[str] = []
        for line in quote_lines:
            cost = len(line) + (1 if included else 0)
            if remaining < cost:
                break
            remaining -= cost
            included.append(line)

        result += block_header + "\n".join(included) + block_footer

    return (result + itogo) if result else "Нет записей"


def _purchase_action(tx: TransactionDto) -> str:
    plan_name = tx.plan.name if tx.plan else "?"
    duration = tx.plan.duration if tx.plan else 0
    dur_label = f"{duration} дн." if duration > 0 else "∞"

    match tx.purchase_type:
        case PurchaseType.NEW:
            return f"🛒 «{plan_name}» ({dur_label})"
        case PurchaseType.RENEW:
            return f"🔄 «{plan_name}» ({dur_label})"
        case PurchaseType.CHANGE:
            return f"🔃 → «{plan_name}» ({dur_label})"
        case PurchaseType.TOPUP:
            return "💰 Пополнение"
        case PurchaseType.EXTRA_DEVICES:
            return "📱 Доп. устройства"
        case _:
            return str(tx.purchase_type)


def _format_transactions(
    transactions: list[TransactionDto],
    max_len: int,
    *,
    month: int = 0,
    year: int = 0,
) -> str:
    completed = [
        tx
        for tx in transactions
        if tx.status == TransactionStatus.COMPLETED and tx.created_at
    ]

    if month > 0:
        completed = [tx for tx in completed if tx.created_at.month == month]  # type: ignore[union-attr]
    if year > 0:
        completed = [tx for tx in completed if tx.created_at.year == year]  # type: ignore[union-attr]

    completed.sort(key=lambda tx: tx.created_at, reverse=True)  # type: ignore[arg-type]

    if not completed:
        return "Нет записей"

    max_tid_len = max(
        len(str(tx.user.telegram_id)) for tx in completed if tx.user
    ) if any(tx.user for tx in completed) else 1

    # Итого
    totals: dict[str, Decimal] = defaultdict(Decimal)
    for tx in completed:
        totals[tx.currency.symbol] += tx.pricing.final_amount
    total_count = len(completed)
    parts = [f"{total_count} {_payment_word(total_count)}"]
    for sym, amt in totals.items():
        parts.append(f"{amt:.2f} {sym}")
    itogo = f"\n────────────────────────────\n<b>Итого:</b> {' | '.join(parts)}"

    effective_max = max_len - len(itogo)

    groups: dict[str, list[TransactionDto]] = defaultdict(list)
    for tx in completed:
        groups[_format_date(tx.created_at)].append(tx)  # type: ignore[arg-type]

    result = ""
    for date_key, entries in groups.items():
        quote_lines = []
        for tx in entries:
            time_str = _format_time(tx.created_at)  # type: ignore[arg-type]
            raw_tid = str(tx.user.telegram_id) if tx.user else "?"
            missing = max_tid_len - len(raw_tid)
            pad = " " * (missing * 2)
            tid_link = pad + _tg_link(raw_tid)
            emoji = _purchase_emoji(tx)
            amount_str = f"{tx.pricing.final_amount:.2f} {tx.currency.symbol}"
            quote_lines.append(f"  {time_str} | {tid_link} | {emoji} | {amount_str}")

        sep = "\n\n" if result else ""
        block_header = f"{sep}📅 <b>{date_key}</b>\n<blockquote>"
        block_footer = "</blockquote>"
        remaining = effective_max - len(result) - len(block_header) - len(block_footer)
        if remaining < len(quote_lines[0]):
            break

        included: list[str] = []
        for line in quote_lines:
            cost = len(line) + (1 if included else 0)
            if remaining < cost:
                break
            remaining -= cost
            included.append(line)

        result += block_header + "\n".join(included) + block_footer

    return (result + itogo) if result else "Нет записей"


def _format_subscriptions(
    transactions: list[TransactionDto],
    max_len: int,
    *,
    month: int = 0,
    year: int = 0,
) -> str:
    sub_types = {PurchaseType.NEW, PurchaseType.RENEW, PurchaseType.CHANGE}
    completed = [
        tx
        for tx in transactions
        if tx.status == TransactionStatus.COMPLETED
        and tx.created_at
        and tx.purchase_type in sub_types
    ]

    if month > 0:
        completed = [tx for tx in completed if tx.created_at.month == month]  # type: ignore[union-attr]
    if year > 0:
        completed = [tx for tx in completed if tx.created_at.year == year]  # type: ignore[union-attr]

    completed.sort(key=lambda tx: tx.created_at, reverse=True)  # type: ignore[arg-type]

    if not completed:
        return "Нет записей"

    max_tid_len = max(
        len(str(tx.user.telegram_id)) for tx in completed if tx.user
    ) if any(tx.user for tx in completed) else 1

    durations = [tx.plan.duration for tx in completed if tx.plan and tx.plan.duration]
    max_dur_len = max(len(str(d)) for d in durations) if durations else 1

    # Итого
    new_count = sum(1 for tx in completed if tx.purchase_type == PurchaseType.NEW)
    renew_count = sum(1 for tx in completed if tx.purchase_type == PurchaseType.RENEW)
    change_count = sum(1 for tx in completed if tx.purchase_type == PurchaseType.CHANGE)
    itogo_parts: list[str] = []
    if new_count:
        itogo_parts.append(f"Новых {new_count}")
    if renew_count:
        itogo_parts.append(f"Продлений {renew_count}")
    if change_count:
        itogo_parts.append(f"Изменений {change_count}")
    itogo = f"\n────────────────────────────\n<b>Итого:</b> {' | '.join(itogo_parts)}"

    effective_max = max_len - len(itogo)

    groups: dict[str, list[TransactionDto]] = defaultdict(list)
    for tx in completed:
        groups[_format_date(tx.created_at)].append(tx)  # type: ignore[arg-type]

    result = ""
    for date_key, entries in groups.items():
        quote_lines = []
        for tx in entries:
            time_str = _format_time(tx.created_at)  # type: ignore[arg-type]
            raw_tid = str(tx.user.telegram_id) if tx.user else "?"
            missing = max_tid_len - len(raw_tid)
            pad = " " * (missing * 2)
            tid_link = pad + _tg_link(raw_tid)
            emoji = _purchase_emoji(tx)
            raw_plan = tx.plan.name if tx.plan else "?"
            plan_short = raw_plan[:3]
            dur = tx.plan.duration if tx.plan else 0
            dur_str = str(dur)
            dur_pad = " " * ((max_dur_len - len(dur_str)) * 2)
            quote_lines.append(f"  {time_str} | {tid_link} | {emoji} | {plan_short} | {dur_pad}{dur_str} д.")

        sep = "\n\n" if result else ""
        block_header = f"{sep}📅 <b>{date_key}</b>\n<blockquote>"
        block_footer = "</blockquote>"
        remaining = effective_max - len(result) - len(block_header) - len(block_footer)
        if remaining < len(quote_lines[0]):
            break

        included: list[str] = []
        for line in quote_lines:
            cost = len(line) + (1 if included else 0)
            if remaining < cost:
                break
            remaining -= cost
            included.append(line)

        result += block_header + "\n".join(included) + block_footer

    return (result + itogo) if result else "Нет записей"


def _format_blocks(users: list[UserDto], max_len: int, *, month: int = 0, year: int = 0) -> str:
    blocked = [u for u in users if u.is_blocked and u.updated_at]

    if month > 0:
        blocked = [u for u in blocked if u.updated_at.month == month]  # type: ignore[union-attr]
    if year > 0:
        blocked = [u for u in blocked if u.updated_at.year == year]  # type: ignore[union-attr]

    blocked.sort(key=lambda u: u.updated_at, reverse=True)  # type: ignore[arg-type]

    if not blocked:
        return "Нет заблокированных пользователей"

    groups: dict[str, list[UserDto]] = defaultdict(list)
    for user in blocked:
        groups[_format_date(user.updated_at)].append(user)  # type: ignore[arg-type]

    result = ""
    for date_key, entries in groups.items():
        quote_lines = []
        for user in entries:
            time_str = _format_time(user.updated_at)  # type: ignore[arg-type]
            label = _user_label(user)
            link = _tg_link(user.telegram_id)
            quote_lines.append(f"  {time_str} • {link} ({label})")

        sep = "\n\n" if result else ""
        block_header = f"{sep}📅 <b>{date_key}</b>\n<blockquote>"
        block_footer = "</blockquote>"
        remaining = max_len - len(result) - len(block_header) - len(block_footer)
        if remaining < len(quote_lines[0]):
            break

        included: list[str] = []
        for line in quote_lines:
            cost = len(line) + (1 if included else 0)
            if remaining < cost:
                break
            remaining -= cost
            included.append(line)

        result += block_header + "\n".join(included) + block_footer

    return result if result else "Нет заблокированных пользователей"


# ── Tabs ──────────────────────────────────────────────

TAB_TITLES = [
    "📝 Регистрации",
    "💳 Оплаты",
    "📦 Подписки",
    "🚫 Блокировки",
]


@inject
async def journal_getter(
    dialog_manager: DialogManager,
    i18n: FromDishka[TranslatorRunner],
    users_service: FromDishka[UserService],
    transaction_service: FromDishka[TransactionService],
    **kwargs: Any,
) -> dict[str, Any]:
    widget: Optional[ManagedScroll] = dialog_manager.find("journal")
    if not widget:
        raise ValueError("journal scroll widget not found")

    current_page = await widget.get_page()

    now = datetime.now()
    selected_month = dialog_manager.dialog_data.get("selected_month", now.month)
    selected_year = now.year
    month_name = MONTH_NAMES[selected_month]

    title = f"{TAB_TITLES[current_page]} - {month_name}"
    header = f"<b>{title}</b>\n\n"
    body_max = MAX_CAPTION_LEN - len(header)

    match current_page:
        case 0:
            users = await users_service.get_all()
            body = _format_registrations(users, body_max, month=selected_month, year=selected_year)
        case 1:
            transactions = await transaction_service.get_all()
            body = _format_transactions(transactions, body_max, month=selected_month, year=selected_year)
        case 2:
            transactions = await transaction_service.get_all()
            body = _format_subscriptions(transactions, body_max, month=selected_month, year=selected_year)
        case 3:
            users = await users_service.get_all()
            body = _format_blocks(users, body_max, month=selected_month, year=selected_year)
        case _:
            raise ValueError(f"Invalid journal page: {current_page}")

    months = [
        {"id": str(i), "text": f"[{MONTH_SHORT[i]}]" if i == selected_month else MONTH_SHORT[i]}
        for i in range(1, 13)
    ]

    return {
        "pages": 4,
        "months": months,
        "journal": header + body,
    }


# ── Export ────────────────────────────────────────────

def _plain_text_registrations(users: list[UserDto]) -> str:
    sorted_users = sorted(
        [u for u in users if u.created_at],
        key=lambda u: u.created_at,  # type: ignore[arg-type]
        reverse=True,
    )

    groups: dict[str, list[UserDto]] = defaultdict(list)
    for user in sorted_users:
        groups[_format_date(user.created_at)].append(user)  # type: ignore[arg-type]

    lines: list[str] = ["=== РЕГИСТРАЦИИ ===", ""]
    for date_key, entries in groups.items():
        lines.append(date_key)
        for user in entries:
            time_str = _format_time(user.created_at)  # type: ignore[arg-type]
            label = _user_label(user)
            lines.append(f"  {time_str} - {user.telegram_id} ({label})")
        lines.append("")

    return "\n".join(lines)


def _plain_text_transactions(
    transactions: list[TransactionDto],
    title: str,
    *,
    purchase_types: Optional[set[PurchaseType]] = None,
) -> str:
    completed = [
        tx
        for tx in transactions
        if tx.status == TransactionStatus.COMPLETED and tx.created_at
    ]
    if purchase_types:
        completed = [tx for tx in completed if tx.purchase_type in purchase_types]

    completed.sort(key=lambda tx: tx.created_at, reverse=True)  # type: ignore[arg-type]

    groups: dict[str, list[TransactionDto]] = defaultdict(list)
    for tx in completed:
        groups[_format_date(tx.created_at)].append(tx)  # type: ignore[arg-type]

    lines: list[str] = [f"=== {title} ===", ""]
    for date_key, entries in groups.items():
        lines.append(date_key)
        for tx in entries:
            time_str = _format_time(tx.created_at)  # type: ignore[arg-type]
            tid = tx.user.telegram_id if tx.user else "?"
            action = _purchase_action(tx)
            amount = f"{tx.pricing.final_amount} {tx.currency.symbol}"
            lines.append(f"  {time_str} - {tid} - {action} - {amount}")
        lines.append("")

    return "\n".join(lines)


def _plain_text_subscriptions(transactions: list[TransactionDto]) -> str:
    sub_types = {PurchaseType.NEW, PurchaseType.RENEW, PurchaseType.CHANGE}
    completed = [
        tx
        for tx in transactions
        if tx.status == TransactionStatus.COMPLETED and tx.created_at and tx.purchase_type in sub_types
    ]
    completed.sort(key=lambda tx: tx.created_at, reverse=True)  # type: ignore[arg-type]

    groups: dict[str, list[TransactionDto]] = defaultdict(list)
    for tx in completed:
        groups[_format_date(tx.created_at)].append(tx)  # type: ignore[arg-type]

    lines: list[str] = ["=== ПОДПИСКИ ===", ""]
    for date_key, entries in groups.items():
        lines.append(date_key)
        for tx in entries:
            time_str = _format_time(tx.created_at)  # type: ignore[arg-type]
            tid = tx.user.telegram_id if tx.user else "?"
            emoji = _purchase_emoji(tx)
            plan_name = tx.plan.name if tx.plan else "?"
            dur = tx.plan.duration if tx.plan else 0
            lines.append(f"  {time_str} - {tid} - {emoji} {plan_name} - {dur} д.")
        lines.append("")

    return "\n".join(lines)


def _plain_text_blocks(users: list[UserDto]) -> str:
    blocked = [u for u in users if u.is_blocked and u.updated_at]
    blocked.sort(key=lambda u: u.updated_at, reverse=True)  # type: ignore[arg-type]

    lines: list[str] = ["=== БЛОКИРОВКИ ===", ""]
    for user in blocked:
        date_str = _format_date(user.updated_at)  # type: ignore[arg-type]
        time_str = _format_time(user.updated_at)  # type: ignore[arg-type]
        label = _user_label(user)
        lines.append(f"  {date_str} {time_str} - {user.telegram_id} ({label})")

    return "\n".join(lines)


async def generate_journal_file(
    users_service: UserService,
    transaction_service: TransactionService,
) -> BufferedInputFile:
    users = await users_service.get_all()
    transactions = await transaction_service.get_all()

    sections = [
        _plain_text_registrations(users),
        _plain_text_transactions(transactions, "ОПЛАТЫ"),
        _plain_text_subscriptions(transactions),
        _plain_text_blocks(users),
    ]

    content = "\n\n".join(sections)
    buf = BytesIO(content.encode("utf-8"))
    return BufferedInputFile(buf.getvalue(), filename="journal.txt")
