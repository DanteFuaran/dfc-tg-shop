from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Group, NumberedPager, Row, Select, StubScroll
from aiogram_dialog.widgets.text import Format

from src.bot.keyboards import main_menu_button
from src.bot.states import Dashboard, DashboardJournal
from src.bot.widgets import Banner, ColoredStart, I18nFormat, IgnoreUpdate

from .getters import journal_getter
from .handlers import on_download_journal, on_month_selected

journal = Window(
    Banner(),
    I18nFormat("msg-journal-main"),
    StubScroll(id="journal", pages="pages"),
    Group(
        Select(
            text=Format("{item[text]}"),
            id="month_select",
            items="months",
            item_id_getter=lambda item: item["id"],
            on_click=on_month_selected,
        ),
        width=6,
    ),
    NumberedPager(
        page_text=I18nFormat("btn-journal-page"),
        current_page_text=I18nFormat("btn-journal-current-page"),
        scroll="journal",
    ),
    Row(
        Button(
            text=I18nFormat("btn-journal-download"),
            id="download_journal",
            on_click=on_download_journal,
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
    state=DashboardJournal.MAIN,
    getter=journal_getter,
)

router = Dialog(journal)
