# Monitoring has been moved to DashboardStatistics module.
# This stub dialog is kept to avoid FSM state restore errors for DashboardRemnawave.MAIN.
from aiogram_dialog import Dialog, StartMode, Window
from aiogram_dialog.widgets.kbd import Row

from src.bot.keyboards import main_menu_button
from src.bot.states import Dashboard, DashboardRemnawave
from src.bot.widgets import Banner, ColoredStart, I18nFormat, IgnoreUpdate


stub = Window(
    Banner(),
    I18nFormat("msg-broadcast-main"),
    Row(
        ColoredStart(
            text=I18nFormat("btn-back"),
            id="back",
            state=Dashboard.MAIN,
            mode=StartMode.RESET_STACK,
            style="primary",
        ),
        *main_menu_button,
    ),
    IgnoreUpdate(),
    state=DashboardRemnawave.MAIN,
)

router = Dialog(stub)
