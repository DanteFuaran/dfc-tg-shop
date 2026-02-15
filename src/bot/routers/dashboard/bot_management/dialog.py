from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row, Start
from aiogram_dialog.widgets.text import Const
from magic_filter import F

from src.bot.keyboards import main_menu_button
from src.bot.routers.dashboard.telegram.handlers import on_logs_request
from src.bot.states import Dashboard, DashboardBotManagement
from src.bot.widgets import Banner, I18nFormat, IgnoreUpdate
from .handlers import (
    bot_management_getter,
    on_check_update,
    on_restart_bot,
    on_back_to_dashboard,
)


bot_management_window = Window(
    Banner(),
    I18nFormat("msg-bot-management"),
    Button(
        text=I18nFormat("btn-remnashop-logs"),
        id="logs",
        on_click=on_logs_request,
    ),
    Button(
        text=I18nFormat("btn-bot-check-update"),
        id="check_update",
        on_click=on_check_update,
    ),
    Button(
        text=I18nFormat("btn-bot-restart"),
        id="restart_bot",
        on_click=on_restart_bot,
    ),
    Row(
        Button(
            text=I18nFormat("btn-back"),
            id="back",
            on_click=on_back_to_dashboard,
        ),
        *main_menu_button,
    ),
    IgnoreUpdate(),
    state=DashboardBotManagement.MAIN,
    getter=bot_management_getter,
)

dialog = Dialog(bot_management_window)
