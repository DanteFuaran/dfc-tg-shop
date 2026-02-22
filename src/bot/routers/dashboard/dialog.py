from aiogram_dialog import Dialog, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Row, Start, SwitchTo
from magic_filter import F

from src.bot.keyboards import main_menu_button
from src.bot.routers.dashboard.handlers import on_save_database
from src.bot.routers.dashboard.getters import dashboard_main_getter
from src.bot.states import (
    Dashboard,
    DashboardAccess,
    DashboardBotManagement,
    DashboardBroadcast,
    DashboardFeatures,
    DashboardImporter,
    DashboardPromocodes,
    DashboardSettings,
    DashboardTelegram,
    DashboardRemnawave,
    DashboardStatistics,
    DashboardUsers,
    DashboardDB,
    TelegramPlans,
)
from src.bot.widgets import Banner, ColoredSwitchTo, I18nFormat, IgnoreUpdate
from src.core.constants import IS_SUPER_DEV_KEY, MIDDLEWARE_DATA_KEY, USER_KEY

dashboard = Window(
    Banner(),
    I18nFormat("msg-dashboard-main"),
    Row(
        SwitchTo(
            text=I18nFormat("btn-dashboard-user-management"),
            id="user_management",
            state=Dashboard.USER_MANAGEMENT,
        ),
        Start(
            text=I18nFormat("btn-dashboard-broadcast"),
            id="broadcast",
            state=DashboardBroadcast.MAIN,
            mode=StartMode.RESET_STACK,
        ),
    ),
    Row(
        Start(
            text=I18nFormat("btn-dashboard-plans"),
            id="plans",
            state=TelegramPlans.MAIN,
            mode=StartMode.RESET_STACK,
        ),
    ),
    Row(
        Start(
            text=I18nFormat("btn-dashboard-payment-settings"),
            id="payment_settings",
            state=DashboardSettings.FINANCES,
            mode=StartMode.RESET_STACK,
        ),
    ),
    Row(
        Start(
            text=I18nFormat("btn-dashboard-settings"),
            id="settings",
            state=DashboardSettings.MAIN,
            mode=StartMode.RESET_STACK,
        ),
    ),
    Row(
        Start(
            text=I18nFormat("btn-dashboard-statistics"),
            id="statistics",
            state=DashboardStatistics.MAIN,
        ),
        Start(
            text=I18nFormat("btn-dashboard-remnawave"),
            id="remnawave",
            state=DashboardRemnawave.MAIN,
            mode=StartMode.RESET_STACK,
        ),
    ),
    Row(
        Start(
            text=I18nFormat("btn-dashboard-bot-management"),
            id="bot_management",
            state=DashboardBotManagement.MAIN,
        ),
        Start(
            text=I18nFormat("btn-dashboard-db"),
            id="db_management",
            state=DashboardDB.MAIN,
        ),
    ),
    Row(
        *main_menu_button,
    ),
    IgnoreUpdate(),
    state=Dashboard.MAIN,
    getter=dashboard_main_getter,
)

user_management = Window(
    Banner(),
    I18nFormat("msg-dashboard-user-management"),
    Row(
        Start(
            text=I18nFormat("btn-dashboard-users"),
            id="users",
            state=DashboardUsers.MAIN,
            mode=StartMode.RESET_STACK,
        ),
        Start(
            text=I18nFormat("btn-remnashop-admins"),
            id="admins",
            state=DashboardTelegram.ADMINS,
            mode=StartMode.RESET_STACK,
        ),
    ),
    Row(
        ColoredSwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=Dashboard.MAIN,
            style="primary",
        ),
        *main_menu_button,
    ),
    IgnoreUpdate(),
    state=Dashboard.USER_MANAGEMENT,
    getter=dashboard_main_getter,
)

router = Dialog(dashboard, user_management)