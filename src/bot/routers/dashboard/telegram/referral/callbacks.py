"""Callback handlers для реферальной системы."""
from typing import cast

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from dishka import FromDishka
from dishka.integrations.aiogram import inject
from fluentogram import TranslatorRunner
from loguru import logger

from src.core.utils.formatters import format_user_log as log
from src.infrastructure.database.models.dto import UserDto

router = Router(name=__name__)


@router.callback_query(F.data == "close_preview")
@inject
async def on_close_preview(
    callback: CallbackQuery,
    user: UserDto,
    i18n: FromDishka[TranslatorRunner],
) -> None:
    """Закрытие сообщения с предпросмотром приглашения."""
    message: Message = cast(Message, callback.message)
    message_id = message.message_id

    logger.info(f"{log(user)} Closed invite preview '{message_id}'")

    try:
        await message.delete()
        await callback.answer()
        logger.debug(f"Preview message '{message_id}' for user '{user.telegram_id}' deleted")
    except Exception as exception:
        logger.error(f"Failed to delete preview message '{message_id}'. Exception: {exception}")
        try:
            await callback.answer(i18n.get("ntf-delete-msg-error"))
        except Exception:
            pass
