from aiogram_dialog import Dialog, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Row, Start
from aiogram_dialog.widgets.text import Const
from magic_filter import F

from src.bot.keyboards import main_menu_button
from src.bot.routers.dashboard.telegram.handlers import on_logs_request
from src.bot.states import Dashboard, DashboardAccess, DashboardBotManagement, DashboardMirrorBots, TelegramNotifications
from src.bot.widgets import Banner, ColoredButton, I18nFormat, IgnoreUpdate
from src.bot.routers.dashboard.settings.handlers import (
    on_toggle_access,
    on_toggle_notifications,
)
from .handlers import (
    bot_management_getter,
    on_check_update,
    on_restart_bot,
    on_back_to_dashboard,
)


bot_management_window = Window(
    Banner(),
    I18nFormat("msg-bot-management"),
    # 1. Режим доступа
    Row(
        Start(
            text=I18nFormat("btn-settings-access"),
            id="access",
            state=DashboardAccess.MAIN,
            mode=StartMode.RESET_STACK,
        ),
        Button(
            text=I18nFormat(
                "btn-settings-toggle",
                enabled=F["access_enabled"],
            ),
            id="toggle_access",
            on_click=on_toggle_access,
        ),
    ),
    # 2. Уведомления
    Row(
        Start(
            text=I18nFormat("btn-settings-notifications"),
            id="notifications",
            state=TelegramNotifications.MAIN,
        ),
        Button(
            text=I18nFormat(
                "btn-settings-toggle",
                enabled=F["notifications_enabled"],
            ),
            id="toggle_notifications",
            on_click=on_toggle_notifications,
        ),
    ),
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
