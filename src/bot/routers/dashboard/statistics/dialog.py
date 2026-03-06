from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import NumberedPager, Row, Start, StubScroll, SwitchTo

from src.bot.keyboards import main_menu_button
from src.bot.states import Dashboard, DashboardStatistics
from src.bot.widgets import Banner, ColoredStart, ColoredSwitchTo, I18nFormat, IgnoreUpdate

from .getters import monitoring_getter, statistics_getter

# Главное окно: выбор раздела
main = Window(
    Banner(),
    I18nFormat("msg-statistics-hub"),
    Row(
        SwitchTo(
            text=I18nFormat("btn-statistics-monitoring"),
            id="monitoring",
            state=DashboardStatistics.MONITORING,
        ),
        SwitchTo(
            text=I18nFormat("btn-statistics-user-stats"),
            id="user_stats",
            state=DashboardStatistics.USER_STATS,
        ),
    ),
    Row(
        ColoredStart(
            text=I18nFormat("btn-back"),
            id="back",
            state=Dashboard.MAIN,
            style="primary",
        ),
        *main_menu_button,
    ),
    IgnoreUpdate(),
    state=DashboardStatistics.MAIN,
)

# Окно мониторинга
monitoring = Window(
    Banner(),
    I18nFormat("msg-monitoring"),
    Row(
        ColoredSwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=DashboardStatistics.MAIN,
            style="primary",
        ),
    ),
    IgnoreUpdate(),
    state=DashboardStatistics.MONITORING,
    getter=monitoring_getter,
)

# Окно статистики по пользователям (бывший MAIN)
user_stats = Window(
    Banner(),
    I18nFormat("msg-statistics-main"),
    StubScroll(id="statistics", pages="pages"),
    NumberedPager(
        page_text=I18nFormat("btn-statistics-page"),
        current_page_text=I18nFormat("btn-statistics-current-page"),
        scroll="statistics",
    ),
    Row(
        ColoredSwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=DashboardStatistics.MAIN,
            style="primary",
        ),
        *main_menu_button,
    ),
    IgnoreUpdate(),
    state=DashboardStatistics.USER_STATS,
    getter=statistics_getter,
    preview_data=statistics_getter,
)

router = Dialog(main, monitoring, user_stats)
