from aiogram_dialog import Dialog, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Row, Start
from aiogram_dialog.widgets.text import Const
from magic_filter import F

from src.bot.keyboards import main_menu_button
from src.bot.routers.dashboard.telegram.handlers import on_logs_request
from src.bot.states import Dashboard, DashboardBotManagement, DashboardMirrorBots
from src.bot.widgets import Banner, ColoredButton, I18nFormat, IgnoreUpdate
from .handlers import (
    bot_management_getter,
    on_check_update,
    on_restart_bot,
    on_back_to_dashboard,
)


bot_management_window = Window(
    Banner(),
    I18nFormat("msg-bot-management"),
    Start(
        text=I18nFormat("btn-mirror-bots"),
        id="mirror_bots",
        state=DashboardMirrorBots.MAIN,
        mode=StartMode.RESET_STACK,
    ),
    Row(
        Button(
            text=I18nFormat("btn-bot-check-update"),
            id="check_update",
            on_click=on_check_update,
        ),
        Button(
            text=I18nFormat("btn-remnashop-logs"),
            id="logs",
            on_click=on_logs_request,
        ),
    ),
    Button(
        text=I18nFormat("btn-bot-restart"),
        id="restart_bot",
        on_click=on_restart_bot,
    ),
    Row(
        ColoredButton(
            text=I18nFormat("btn-back"),
            id="back",
            on_click=on_back_to_dashboard,
            style="primary",
        ),
        *main_menu_button,
    ),
    IgnoreUpdate(),
    state=DashboardBotManagement.MAIN,
    getter=bot_management_getter,
)

dialog = Dialog(bot_management_window)
