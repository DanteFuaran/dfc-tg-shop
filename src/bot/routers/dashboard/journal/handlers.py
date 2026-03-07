from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.services.transaction import TransactionService
from src.services.user import UserService

from .getters import generate_journal_file


async def on_month_selected(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    item_id: str,
) -> None:
    manager.dialog_data["selected_month"] = int(item_id)


CLOSE_JOURNAL_CB = "close_journal_file"

close_router = Router()


@inject
async def on_download_journal(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
    users_service: FromDishka[UserService],
    transaction_service: FromDishka[TransactionService],
) -> None:
    file = await generate_journal_file(
        users_service=users_service,
        transaction_service=transaction_service,
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Закрыть", callback_data=CLOSE_JOURNAL_CB)]
        ]
    )
    await callback.message.answer_document(file, reply_markup=keyboard)  # type: ignore[union-attr]
    await callback.answer()


@close_router.callback_query(F.data == CLOSE_JOURNAL_CB)
async def on_close_journal_file(callback: CallbackQuery) -> None:
    if callback.message:
        await callback.message.delete()
    await callback.answer()
