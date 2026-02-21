from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import ShowMode
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
    bot = dialog_manager.middleware_data.get("bot")
    main_bot_info = await bot.get_me()
    main_username = main_bot_info.username or "main_bot"

    bots = await mirror_bot_service.get_all()
    any_mirror_primary = any(b.is_primary for b in bots)
    main_is_primary = not any_mirror_primary

    # Main bot always first
    main_item = {
        "id": "main",
        "username": f"@{main_username}",
        "is_primary": main_is_primary,
        "is_main": True,
        "display": f"{'🔘' if main_is_primary else '⚪'} {main_username}",
        "right_label": "Системный",
    }
    mirror_items = [
        {
            "id": str(b.id),
            "username": f"@{b.username}",
            "is_primary": b.is_primary,
            "is_main": False,
            "display": f"{'🔘' if b.is_primary else '⚪'} {b.username}",
            "right_label": "Удалить",
        }
        for b in bots
    ]
    items = [main_item] + mirror_items
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


@inject
async def on_select_mirror_bot(
    callback: CallbackQuery,
    widget: Button,
    sub_manager: SubManager,
    mirror_bot_service: FromDishka[MirrorBotService],
) -> None:
    """Toggle primary status for a mirror bot."""
    item_id = sub_manager.item_id
    current_bots = await mirror_bot_service.get_all()

    if item_id == "main":
        # Main bot selected — reset mirror primary so main bot is used
        any_mirror_primary = any(b.is_primary for b in current_bots)
        if any_mirror_primary:
            await mirror_bot_service.set_primary(None)
            await callback.answer("✅ Используется основной бот")
        else:
            await callback.answer("ℹ️ Уже используется основной бот")
        return

    mirror_bot_id = int(item_id)
    already_primary = any(b.is_primary and b.id == mirror_bot_id for b in current_bots)

    if already_primary:
        await mirror_bot_service.set_primary(None)
        await callback.answer("✅ Основной бот сброшен — используется главный бот")
    else:
        await mirror_bot_service.set_primary(mirror_bot_id)
        username = next((b.username for b in current_bots if b.id == mirror_bot_id), "?")
        await callback.answer(f"✅ @{username} назначен основным ботом")


@inject
async def on_action_bot(
    callback: CallbackQuery,
    widget: Button,
    sub_manager: SubManager,
    mirror_bot_service: FromDishka[MirrorBotService],
) -> None:
    """Handle right-column action: ignore for main bot, delete for mirror bots."""
    item_id = sub_manager.item_id

    if item_id == "main":
        await callback.answer("ℹ️ Основной бот системы — нельзя удалить")
        return

    user = sub_manager.middleware_data.get(USER_KEY)
    mirror_bot_id = int(item_id)

    mirror_bot_manager = sub_manager.middleware_data.get("mirror_bot_manager")
    if mirror_bot_manager:
        await mirror_bot_manager.stop_mirror_bot(mirror_bot_id)

    username = await mirror_bot_service.remove(mirror_bot_id)
    if username:
        logger.info(f"{log(user)} Removed mirror bot @{username}")
        await callback.answer(f"Бот @{username} удалён")
    else:
        await callback.answer("Бот не найден")


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

    # Clear previous error
    manager.dialog_data.pop("add_error", None)

    if ":" not in token:
        manager.dialog_data["add_error"] = "Невалидный формат токена. Используйте формат: 123456:ABC-DEF..."
        return

    try:
        mirror_bot = await mirror_bot_service.add(token)
        logger.info(f"{log(user)} Added mirror bot @{mirror_bot.username}")

        # Start the mirror bot immediately if MirrorBotManager is available
        mirror_bot_manager = manager.middleware_data.get("mirror_bot_manager")
        if mirror_bot_manager and mirror_bot.id is not None:
            dispatcher = manager.middleware_data.get("aiogd_original_dispatcher") or manager.middleware_data.get("dispatcher")
            allowed_updates = dispatcher.resolve_used_update_types() if dispatcher else []
            await mirror_bot_manager.start_mirror_bot(mirror_bot, allowed_updates)

        # Delete old dialog message (token input) and send fresh MAIN message
        manager.show_mode = ShowMode.DELETE_AND_SEND
        await manager.switch_to(DashboardMirrorBots.MAIN)

    except ValueError as e:
        manager.dialog_data["add_error"] = str(e)
    except Exception as e:
        logger.error(f"Error adding mirror bot: {e}")
        manager.dialog_data["add_error"] = "Произошла внутренняя ошибка. Попробуйте позже."


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
    manager.dialog_data.pop("add_error", None)
    manager.show_mode = ShowMode.DELETE_AND_SEND
    await manager.switch_to(DashboardMirrorBots.MAIN)


async def add_token_getter(
    dialog_manager: DialogManager,
    **kwargs: Any,
) -> dict[str, Any]:
    """Getter for add-token window — passes dialog_data error if set."""
    return {
        "add_error": dialog_manager.dialog_data.get("add_error", ""),
    }
