from aiogram_dialog import Dialog, StartMode, Window, ShowMode
from aiogram_dialog.widgets.kbd import Button, Row, Start, Column, ListGroup, Group, SwitchTo
from aiogram_dialog.widgets.text import Format, Const
from magic_filter import F

from src.bot.keyboards import main_menu_button
from src.bot.states import Dashboard, DashboardImporter
from src.bot.widgets import Banner, I18nFormat, IgnoreUpdate
from .handlers import (
    on_save_db,
    on_load_db,
    on_db_file_input,
    on_convert_db,
    backups_getter,
    on_restore_backup,
    on_export_db,
    on_import_db,
    on_back_to_dashboard,
    on_delete_backup,
    on_export_backup_to_db,
    on_sync_from_bot,
    on_sync_from_panel,
    on_sync_manage,
    on_remnawave_import,
    sync_getter,
    on_clear_all,
    on_clear_users,
)
from src.bot.states import DashboardDB
db_management = Window(
    Banner(),
    I18nFormat("msg-db-main"),
    Row(
        Button(
            text=I18nFormat("btn-db-save"),
            id="save_db",
            on_click=on_save_db,
        ),
        Button(
            text=I18nFormat("btn-db-load"),
            id="load_db",
            on_click=on_load_db,
        ),
    ),
    Row(
        Button(
            text=I18nFormat("btn-db-clear-all"),
            id="clear_all",
            on_click=on_clear_all,
        ),
        Button(
            text=I18nFormat("btn-db-clear-users"),
            id="clear_users",
            on_click=on_clear_users,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-db-imports"),
            id="imports",
            state=DashboardDB.IMPORTS,
        ),
        SwitchTo(
            text=I18nFormat("btn-db-sync"),
            id="sync",
            state=DashboardDB.SYNC,
        ),
    ),
    Row(
        Button(
            text=I18nFormat("btn-back"),
            id="back",
            on_click=on_back_to_dashboard,
        ),
        *main_menu_button,
    ),
    IgnoreUpdate(),
    state=DashboardDB.MAIN,
)

# Window for uploading DB dump file
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput

db_load_window = Window(
    Banner(),
    I18nFormat("msg-db-load"),
    ListGroup(
        Row(
            Button(
                text=Format("📄"),
                id="export_to_db",
                on_click=on_export_backup_to_db,
            ),
            Button(
                text=Format("{item[name]}"),
                id="restore",
                on_click=on_restore_backup,
            ),
            Button(
                text=Format("❌"),
                id="delete",
                on_click=on_delete_backup,
            ),
        ),
        id="backups_list",
        item_id_getter=lambda item: item["index"],
        items="backups",
    ),
    Row(
        Button(
            text=I18nFormat("btn-back"),
            id="back",
            on_click=on_back_to_dashboard,
        ),
        *main_menu_button,
    ),
    IgnoreUpdate(),
    state=DashboardDB.LOAD,
    getter=backups_getter,
)

# Окно выбора направления синхронизации
db_sync_window = Window(
    Banner(),
    I18nFormat("msg-db-sync"),
    Row(
        Button(
            text=I18nFormat("btn-db-sync-remnawave-to-bot"),
            id="sync_from_panel",
            on_click=on_sync_from_panel,
        ),
        Button(
            text=I18nFormat("btn-db-sync-bot-to-remnawave"),
            id="sync_from_bot",
            on_click=on_sync_from_bot,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=DashboardDB.MAIN,
        ),
        *main_menu_button,
    ),
    IgnoreUpdate(),
    state=DashboardDB.SYNC,
)

# Окно процесса синхронизации
db_sync_progress = Window(
    Banner(),
    I18nFormat("msg-db-sync-progress"),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=DashboardDB.SYNC,
        ),
        *main_menu_button,
    ),
    IgnoreUpdate(),
    state=DashboardDB.SYNC_PROGRESS,
    getter=sync_getter,
)

# Окно подтверждения полной очистки базы

# Окно подтверждения очистки пользователей
clear_users_confirm = Window(
    Banner(),
    I18nFormat("msg-db-clear-users-confirm"),
    Row(
        Button(
            text=I18nFormat("btn-db-clear-users"),
            id="confirm_clear_users",
            on_click=on_clear_users,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-cancel"),
            id="cancel",
            state=DashboardDB.MAIN,
        ),
    ),
    IgnoreUpdate(),
    state=DashboardDB.CLEAR_USERS_CONFIRM,
)

# Меню импортов
imports_menu = Window(
    Banner(),
    I18nFormat("msg-db-imports"),
    Column(
        Button(
            text=I18nFormat("btn-db-remnawave-import"),
            id="remnawave_import",
            on_click=on_remnawave_import,
        ),
        Start(
            text=I18nFormat("btn-db-xui-import"),
            id="importer",
            state=DashboardImporter.MAIN,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=DashboardDB.MAIN,
        ),
        *main_menu_button,
    ),
    IgnoreUpdate(),
    state=DashboardDB.IMPORTS,
)

dialog = Dialog(
    db_management,
    db_load_window,
    db_sync_window,
    db_sync_progress,
    clear_users_confirm,
    imports_menu,
)
