from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.kbd.list_group import SubManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from loguru import logger

from src.bot.states import DashboardBotManagement, DashboardMirrorBots
from src.core.constants import USER_KEY
from src.core.utils.formatters import format_user_log as log
from src.infrastructure.database import UnitOfWork
from src.infrastructure.database.models.dto.mirror_bot import MirrorBotDto
from src.services.mirror_bot import MirrorBotService


@inject
async def mirror_bots_getter(
    dialog_manager: DialogManager,
    mirror_bot_service: FromDishka[MirrorBotService],
    **kwargs: Any,
) -> dict[str, Any]:
    """Getter for mirror bots list window."""
    bots = await mirror_bot_service.get_all()
    items = [
        {
            "id": str(b.id),
            "username": f"@{b.username}",
            "active": b.is_active,
        }
        for b in bots
    ]
    return {
        "mirror_bots": items,
        "has_bots": len(items) > 0,
    }


async def on_back_to_bot_management(
    callback: CallbackQuery,
    button: Any,
    manager: DialogManager,
) -> None:
    """Go back to bot management menu."""
    await manager.start(DashboardBotManagement.MAIN)


async def on_add_mirror_bot(
    callback: CallbackQuery,
    button: Any,
    manager: DialogManager,
) -> None:
    """Switch to token input state."""
    await manager.switch_to(DashboardMirrorBots.ADD_TOKEN)


@inject
async def on_token_input(
    message: Message,
    widget: Any,
    manager: DialogManager,
    value: str,
    mirror_bot_service: FromDishka[MirrorBotService],
) -> None:
    """Handle token input from user."""
    user = manager.middleware_data.get(USER_KEY)
    token = value.strip()

    # Delete user's message with the token for security
    try:
        await message.delete()
    except Exception:
        pass

    if ":" not in token:
        await message.answer("❌ <b>Невалидный формат токена.</b>\n\nТокен должен быть в формате: <code>123456:ABC-DEF...</code>")
        return

    try:
        mirror_bot = await mirror_bot_service.add(token)
        logger.info(f"{log(user)} Added mirror bot @{mirror_bot.username}")

        # Start the mirror bot immediately if MirrorBotManager is available
        started = False
        mirror_bot_manager = manager.middleware_data.get("mirror_bot_manager")
        if mirror_bot_manager and mirror_bot.id is not None:
            dispatcher = manager.middleware_data.get("aiogd_original_dispatcher") or manager.middleware_data.get("dispatcher")
            if dispatcher:
                allowed_updates = dispatcher.resolve_used_update_types()
            else:
                allowed_updates = []
            started = await mirror_bot_manager.start_mirror_bot(mirror_bot, allowed_updates)

        if started:
            await message.answer(
                f"✅ <b>Бот @{mirror_bot.username} успешно добавлен и запущен!</b>",
            )
        else:
            await message.answer(
                f"✅ <b>Бот @{mirror_bot.username} добавлен!</b>\n\n"
                f"⚠️ Бот будет активирован после перезапуска основного бота.",
            )
        await manager.switch_to(DashboardMirrorBots.MAIN)
    except ValueError as e:
        await message.answer(f"❌ <b>Ошибка:</b> {e}")
    except Exception as e:
        logger.error(f"Error adding mirror bot: {e}")
        await message.answer("❌ <b>Произошла ошибка при добавлении бота.</b>")


@inject
async def on_delete_mirror_bot(
    callback: CallbackQuery,
    widget: Button,
    sub_manager: SubManager,
    mirror_bot_service: FromDishka[MirrorBotService],
) -> None:
    """Delete a mirror bot."""
    user = sub_manager.middleware_data.get(USER_KEY)
    mirror_bot_id = int(sub_manager.item_id)

    # Stop the running mirror bot first
    mirror_bot_manager = sub_manager.middleware_data.get("mirror_bot_manager")
    if mirror_bot_manager:
        await mirror_bot_manager.stop_mirror_bot(mirror_bot_id)

    username = await mirror_bot_service.remove(mirror_bot_id)
    if username:
        logger.info(f"{log(user)} Removed mirror bot @{username}")
        await callback.answer(f"Бот @{username} удалён")
    else:
        await callback.answer("Бот не найден")


async def on_cancel_add(
    callback: CallbackQuery,
    button: Any,
    manager: DialogManager,
) -> None:
    """Cancel adding a new mirror bot."""
    await manager.switch_to(DashboardMirrorBots.MAIN)
