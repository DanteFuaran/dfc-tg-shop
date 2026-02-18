from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Column, Row, Select, Start, SwitchTo
from magic_filter import F

from src.bot.keyboards import main_menu_button
from src.bot.states import DashboardTelegram, TelegramNotifications
from src.bot.widgets import Banner, ColoredButton, I18nFormat, IgnoreUpdate
from src.core.enums import SystemNotificationType, UserNotificationType

from .getters import system_types_getter, user_types_getter
from .handlers import (
    on_system_type_select,
    on_user_type_select,
    on_notifications_cancel_main,
    on_notifications_accept_main,
    on_notifications_cancel_submenu,
    on_notifications_accept_submenu,
)

notifications = Window(
    Banner(),
    I18nFormat("msg-notifications-main"),
    Row(
        SwitchTo(
            text=I18nFormat("btn-notifications-user"),
            id="users",
            state=TelegramNotifications.USER,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-notifications-system"),
            id="system",
            state=TelegramNotifications.SYSTEM,
        ),
    ),
    Row(
        ColoredButton(
            text=I18nFormat("btn-cancel"),
            id="cancel",
            on_click=on_notifications_cancel_main,
            style="danger",
        ),
        ColoredButton(
            text=I18nFormat("btn-accept"),
            id="accept",
            on_click=on_notifications_accept_main,
            style="success",
        ),
    ),
    IgnoreUpdate(),
    state=TelegramNotifications.MAIN,
)

user = Window(
    Banner(),
    I18nFormat("msg-notifications-user"),
    Column(
        Select(
            text=I18nFormat(
                "btn-notifications-user-choice",
                type=F["item"]["type"],
                enabled=F["item"]["enabled"],
            ),
            id="select_type",
            item_id_getter=lambda item: item["type"],
            items="types",
            type_factory=UserNotificationType,
            on_click=on_user_type_select,
        ),
    ),
    Row(
        ColoredButton(
            text=I18nFormat("btn-cancel"),
            id="cancel",
            on_click=on_notifications_cancel_submenu,
            style="danger",
        ),
        ColoredButton(
            text=I18nFormat("btn-accept"),
            id="accept",
            on_click=on_notifications_accept_submenu,
            style="success",
        ),
    ),
    IgnoreUpdate(),
    state=TelegramNotifications.USER,
    getter=user_types_getter,
)

system = Window(
    Banner(),
    I18nFormat("msg-notifications-system"),
    Column(
        Select(
            text=I18nFormat(
                "btn-notifications-system-choice",
                type=F["item"]["type"],
                enabled=F["item"]["enabled"],
            ),
            id="select_type",
            item_id_getter=lambda item: item["type"],
            items="types",
            type_factory=SystemNotificationType,
            on_click=on_system_type_select,
        ),
    ),
    Row(
        ColoredButton(
            text=I18nFormat("btn-cancel"),
            id="cancel",
            on_click=on_notifications_cancel_submenu,
            style="danger",
        ),
        ColoredButton(
            text=I18nFormat("btn-accept"),
            id="accept",
            on_click=on_notifications_accept_submenu,
            style="success",
        ),
    ),
    IgnoreUpdate(),
    state=TelegramNotifications.SYSTEM,
    getter=system_types_getter,
)

router = Dialog(
    notifications,
    user,
    system,
)
