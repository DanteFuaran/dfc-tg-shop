from aiogram_dialog import Dialog, StartMode, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Column,
    CopyText,
    Group,
    ListGroup,
    Row,
    Select,
    Start,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Format
from magic_filter import F

from src.bot.keyboards import main_menu_button
from src.bot.states import DashboardTelegram, TelegramGateways, DashboardSettings
from src.bot.widgets import Banner, ColoredButton, ColoredSwitchTo, I18nFormat, IgnoreUpdate
from src.core.enums import Currency
from .handlers import (
    on_active_toggle,
    on_default_currency_select,
    on_field_input,
    on_field_select,
    on_gateway_move,
    on_gateway_select,
    on_gateway_test,
    on_gateways_cancel,
    on_gateways_accept,
    on_placement_cancel,
    on_placement_accept,
    on_currency_cancel,
    on_currency_accept,
)

from .getters import (
    currency_getter,
    field_getter,
    gateway_getter,
    gateways_getter,
    placement_getter,
)

gateways = Window(
    Banner(),
    I18nFormat("msg-gateways-main"),
    ListGroup(
        Row(
            Button(
                text=I18nFormat("btn-gateway-title", gateway_type=F["item"]["gateway_type"]),
                id="select_gateway",
                on_click=on_gateway_select,
            ),
            Button(
                text=I18nFormat("btn-gateway-test"),
                id="test_gateway",
                on_click=on_gateway_test,
            ),
            Button(
                text=I18nFormat("btn-gateway-active", is_active=F["item"]["is_active"]),
                id="active_toggle",
                on_click=on_active_toggle,
            ),
        ),
        id="gateways_list",
        item_id_getter=lambda item: item["id"],
        items="gateways",
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-gateways-placement"),
            id="placement",
            state=TelegramGateways.PLACEMENT,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-gateways-default-currency"),
            id="default_currency",
            state=TelegramGateways.CURRENCY,
        ),
    ),
    Row(
        ColoredButton(
            text=I18nFormat("btn-cancel"),
            id="cancel",
            on_click=on_gateways_cancel,
            style="danger",
        ),
        ColoredButton(
            text=I18nFormat("btn-accept"),
            id="accept",
            on_click=on_gateways_accept,
            style="success",
        ),
    ),
    IgnoreUpdate(),
    state=TelegramGateways.MAIN,
    getter=gateways_getter,
)

gateway_settings = Window(
    Banner(),
    I18nFormat("msg-gateways-settings", gateway_type=F["gateway_type"]),
    Group(
        Select(
            text=I18nFormat("btn-gateways-setting", field=F["item"]["field"].upper()),
            id="setting",
            item_id_getter=lambda item: item["field"],
            items="settings",
            type_factory=str,
            on_click=on_field_select,
        ),
        width=2,
    ),
    Row(
        CopyText(
            text=I18nFormat("btn-gateways-webhook-copy"),
            copy_text=Format("{webhook}"),
        ),
        when=F["requires_webhook"],
    ),
    Row(
        ColoredSwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=TelegramGateways.MAIN,
            style="primary",
        ),
    ),
    IgnoreUpdate(),
    state=TelegramGateways.SETTINGS,
    getter=gateway_getter,
)

gateway_field = Window(
    Banner(),
    I18nFormat("msg-gateways-field", gateway_type=F["gateway_type"]),
    Row(
        ColoredSwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=TelegramGateways.SETTINGS,
            style="primary",
        ),
    ),
    MessageInput(func=on_field_input),
    IgnoreUpdate(),
    state=TelegramGateways.FIELD,
    getter=field_getter,
)

default_currency = Window(
    Banner(),
    I18nFormat("msg-gateways-default-currency"),
    Column(
        Select(
            text=I18nFormat(
                "btn-gateways-default-currency-choice",
                symbol=F["item"]["symbol"],
                currency=F["item"]["currency"],
                enabled=F["item"]["enabled"],
            ),
            id="currency",
            item_id_getter=lambda item: item["currency"],
            items="currency_list",
            type_factory=Currency,
            on_click=on_default_currency_select,
        ),
    ),
    Row(
        ColoredButton(
            text=I18nFormat("btn-cancel"),
            id="cancel",
            on_click=on_currency_cancel,
            style="danger",
        ),
        ColoredButton(
            text=I18nFormat("btn-accept"),
            id="accept",
            on_click=on_currency_accept,
            style="success",
        ),
    ),
    IgnoreUpdate(),
    state=TelegramGateways.CURRENCY,
    getter=currency_getter,
)

placement = Window(
    Banner(),
    I18nFormat("msg-gateways-placement"),
    ListGroup(
        Row(
            Button(
                text=I18nFormat("btn-gateway-title", gateway_type=F["item"]["gateway_type"]),
                id="gateway",
            ),
            Button(
                text=Format("🔼"),
                id="move",
                on_click=on_gateway_move,
            ),
        ),
        id="gateways_list",
        item_id_getter=lambda item: item["id"],
        items="gateways",
    ),
    Row(
        ColoredButton(
            text=I18nFormat("btn-cancel"),
            id="cancel",
            on_click=on_placement_cancel,
            style="danger",
        ),
        ColoredButton(
            text=I18nFormat("btn-accept"),
            id="accept",
            on_click=on_placement_accept,
            style="success",
        ),
    ),
    IgnoreUpdate(),
    state=TelegramGateways.PLACEMENT,
    getter=placement_getter,
)

router = Dialog(
    gateways,
    gateway_settings,
    gateway_field,
    default_currency,
    placement,
)
