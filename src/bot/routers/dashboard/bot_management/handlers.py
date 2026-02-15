import asyncio
import subprocess
import time
from typing import Any

import httpx
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from loguru import logger

from src.__version__ import __version__
from src.core.constants import REPOSITORY, USER_KEY, get_update_branch
from src.core.storage.keys import UpdateMessageKey
from src.core.utils.formatters import format_user_log as log
from src.infrastructure.redis.repository import RedisRepository
from src.services.update_checker import (
    UPDATE_CLOSE,
    UPDATE_NOW,
    UpdateCheckerService,
)

_HOST_PROJECT_DIR = "/opt/dfc-tg-shop"

# Track pending restart confirmations: {user_id: (timestamp, message_id)}
_restart_confirmations: dict[int, tuple[float, int]] = {}


def _parse_version(version_str: str) -> tuple[int, ...]:
    try:
        return tuple(int(x) for x in version_str.strip().split("."))
    except (ValueError, AttributeError):
        return (0, 0, 0)


async def bot_management_getter(
    dialog_manager: DialogManager,
    **kwargs: Any,
) -> dict[str, Any]:
    """Getter for bot management page."""
    return {
        "bot_version": __version__,
    }


@inject
async def on_check_update(
    callback: CallbackQuery,
    button: Any,
    manager: DialogManager,
    update_checker_service: FromDishka[UpdateCheckerService],
) -> None:
    """Check for updates. If available, send a notification with Update Now button."""
    user = manager.middleware_data.get(USER_KEY)
    logger.info(f"{log(user)} Checking for updates from bot management menu")

    try:
        branch = get_update_branch()
        url = REPOSITORY.replace("github.com", "raw.githubusercontent.com") + f"/{branch}/assets/update/.update"

        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            remote = ""
            for line in response.text.splitlines():
                if line.startswith("version:"):
                    remote = line.split(":", 1)[1].strip()
                    break

        if _parse_version(remote) > _parse_version(__version__):
            # Update available — send notification with action buttons
            await callback.answer()
            keyboard = InlineKeyboardBuilder()
            keyboard.row(
                InlineKeyboardButton(text="🔄 Обновить сейчас", callback_data=UPDATE_NOW),
            )
            keyboard.row(
                InlineKeyboardButton(text="❌ Закрыть", callback_data=UPDATE_CLOSE),
            )
            await callback.bot.send_message(
                chat_id=callback.from_user.id,
                text=(
                    f"✅ Текущая версия: <code>{__version__}</code>\n"
                    f"⬆️ Доступна версия: <code>{remote}</code>"
                ),
                parse_mode="HTML",
                reply_markup=keyboard.as_markup(),
            )
        else:
            await callback.answer()
            msg = await callback.bot.send_message(
                chat_id=callback.from_user.id,
                text=f"✅ Установлена последняя версия: <code>{__version__}</code>",
                parse_mode="HTML",
            )
            asyncio.create_task(_auto_delete_message(callback.bot, msg, 5))
    except Exception as e:
        logger.error(f"[bot_management] Update check failed: {e}")
        await callback.answer()
        msg = await callback.bot.send_message(
            chat_id=callback.from_user.id,
            text="❌ Не удалось проверить обновления",
        )
        asyncio.create_task(_auto_delete_message(callback.bot, msg, 5))


async def _auto_delete_message(bot, msg, delay: int = 5) -> None:
    """Auto-delete a message after a delay."""
    await asyncio.sleep(delay)
    try:
        await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    except Exception:
        pass


async def _restart_bot_container() -> None:
    """Restart the bot container via Docker."""
    try:
        subprocess.Popen(
            ["docker", "restart", "-t", "30", "dfc-tg"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception as e:
        logger.error(f"[restart] Failed to restart container: {e}")


@inject
async def on_restart_bot(
    callback: CallbackQuery,
    button: Any,
    manager: DialogManager,
    redis_repository: FromDishka[RedisRepository],
) -> None:
    """Restart the bot by stopping the container (docker will auto-restart)."""
    user = manager.middleware_data.get(USER_KEY)
    user_id = callback.from_user.id
    now = time.time()
    bot = callback.bot

    # Check if this is a confirmation (second click within 5 seconds)
    if user_id in _restart_confirmations:
        last_click, warning_msg_id = _restart_confirmations[user_id]
        if now - last_click < 5:
            # Second click within 5s — proceed with restart
            _restart_confirmations.pop(user_id, None)
            logger.info(f"{log(user)} Triggered bot restart from management menu")

            # Answer callback first
            try:
                await callback.answer()
            except Exception:
                pass

            # Delete the warning message before restarting
            try:
                await bot.delete_message(chat_id=user_id, message_id=warning_msg_id)
                logger.debug(f"Deleted restart warning message {warning_msg_id}")
            except Exception as e:
                logger.warning(f"Failed to delete restart warning {warning_msg_id}: {e}")

            # Small delay to ensure Telegram processes the deletion
            await asyncio.sleep(0.3)

            try:
                # Send restart message
                msg = await bot.send_message(
                    chat_id=user_id,
                    text="<b>🔄 Перезапуск бота...</b>\n<i>Бот будет доступен через несколько секунд.</i>",
                    parse_mode="HTML",
                )

                # Save message ref for deletion on startup
                msg_ref = f"{msg.chat.id}:{msg.message_id}"
                await redis_repository.set(UpdateMessageKey(), msg_ref, ex=600)  # TTL 10 min

                # Give the message a moment to be sent, then restart
                asyncio.create_task(_restart_bot_container())
            except Exception as e:
                logger.error(f"[bot_management] Restart failed: {e}")
                msg = await bot.send_message(
                    chat_id=user_id,
                    text="❌ Не удалось перезагрузить бота",
                )
                asyncio.create_task(_auto_delete_message(bot, msg, 5))
            return
        else:
            # 5 seconds expired, remove old confirmation and start new one
            _restart_confirmations.pop(user_id, None)

    # First click — show warning notification
    await callback.answer()
    warning_msg = await bot.send_message(
        chat_id=user_id,
        text="⚠️ <b>При повторном нажатии сервер будет перезагружен.</b>",
        parse_mode="HTML",
    )
    _restart_confirmations[user_id] = (now, warning_msg.message_id)
    
    # Auto-delete warning message after 5 seconds if no second click
    async def _revert_restart_warning() -> None:
        await asyncio.sleep(5)
        if user_id in _restart_confirmations and _restart_confirmations[user_id][0] == now:
            _restart_confirmations.pop(user_id, None)
            try:
                await bot.delete_message(chat_id=user_id, message_id=warning_msg.message_id)
            except Exception:
                pass

    asyncio.create_task(_revert_restart_warning())


async def on_back_to_dashboard(callback: CallbackQuery, button: Any, manager: DialogManager):
    """Go back to the dashboard."""
    from src.bot.states import Dashboard
    await manager.start(Dashboard.MAIN)
