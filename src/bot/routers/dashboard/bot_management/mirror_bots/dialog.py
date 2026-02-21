from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, ListGroup, Row
from aiogram_dialog.widgets.text import Const, Format
from magic_filter import F

from src.bot.keyboards import main_menu_button
from src.bot.states import DashboardMirrorBots
from src.bot.widgets import Banner, ColoredButton, I18nFormat, IgnoreUpdate

from .handlers import (
    add_token_getter,
    mirror_bots_getter,
    on_add_mirror_bot,
    on_back_to_bot_management,
    on_cancel_add,
    on_delete_mirror_bot,
    on_select_mirror_bot,
    on_token_input,
)


# Main window — list of mirror bots
mirror_bots_main = Window(
    Banner(),
    I18nFormat("msg-mirror-bots"),
    ListGroup(
        Row(
            Button(
                text=Format("{item[display]}"),
                id="select_bot",
                on_click=on_select_mirror_bot,
            ),
            Button(
                text=Const("❌"),
                id="delete_bot",
                on_click=on_delete_mirror_bot,
                when=lambda data, widget, manager: not data.get("item", {}).get("is_main", False),
            ),
        ),
        id="mirror_bots_list",
        item_id_getter=lambda item: item["id"],
        items="mirror_bots",
    ),
    Button(
        text=I18nFormat("btn-mirror-bot-add"),
        id="add_mirror_bot",
        on_click=on_add_mirror_bot,
    ),
    Row(
        ColoredButton(
            text=I18nFormat("btn-back"),
            id="back",
            on_click=on_back_to_bot_management,
            style="primary",
        ),
        *main_menu_button,
    ),
    IgnoreUpdate(),
    state=DashboardMirrorBots.MAIN,
    getter=mirror_bots_getter,
)

# Token input window
add_token_window = Window(
    Banner(),
    I18nFormat("msg-mirror-bot-add-token"),
    Format("\n❌ <b>{add_error}</b>", when="add_error"),
    TextInput(
        id="mirror_bot_token",
        on_success=on_token_input,
    ),
    Row(
        ColoredButton(
            text=I18nFormat("btn-cancel"),
            id="cancel",
            on_click=on_cancel_add,
            style="danger",
        ),
        *main_menu_button,
    ),
    IgnoreUpdate(),
    state=DashboardMirrorBots.ADD_TOKEN,
    getter=add_token_getter,
)

dialog = Dialog(
    mirror_bots_main,
    add_token_window,
)
