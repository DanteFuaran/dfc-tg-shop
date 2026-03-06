from aiogram_dialog import Dialog, StartMode, Window
from aiogram_dialog.widgets.kbd import Row

from src.bot.keyboards import main_menu_button
from src.bot.states import Dashboard, DashboardRemnawave
from src.bot.widgets import Banner, ColoredStart, I18nFormat, IgnoreUpdate

from .getters import monitoring_getter

monitoring = Window(
    Banner(),
    I18nFormat("msg-monitoring"),
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
    getter=monitoring_getter,
)

router = Dialog(
    monitoring,
)
