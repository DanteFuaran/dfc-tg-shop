from datetime import datetime
from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner
from remnapy import RemnawaveSDK

from src.core.utils.formatters import format_country_code


@inject
async def monitoring_getter(
    dialog_manager: DialogManager,
    remnawave: FromDishka[RemnawaveSDK],
    i18n: FromDishka[TranslatorRunner],
    **kwargs: Any,
) -> dict[str, Any]:
    stats = await remnawave.system.get_stats()
    nodes_result = await remnawave.nodes.get_all_nodes()

    # Статистика пользователей
    users_total = stats.users.total_users
    users_active = stats.users.status_counts.get("ACTIVE", 0)
    users_disabled = stats.users.status_counts.get("DISABLED", 0)
    users_limited = stats.users.status_counts.get("LIMITED", 0)
    users_expired = stats.users.status_counts.get("EXPIRED", 0)

    online_last_day = stats.online_stats.last_day
    online_last_week = stats.online_stats.last_week
    online_never = stats.online_stats.never_online
    online_now = stats.online_stats.online_now

    # Список серверов (нод)
    total_servers = len(nodes_result)
    available_servers = sum(1 for n in nodes_result if n.is_connected)
    total_online = sum(n.users_online for n in nodes_result)

    server_lines = []
    for node in nodes_result:
        flag = format_country_code(code=node.country_code)
        status_icon = "🟢" if node.is_connected else "🔴"
        server_lines.append(
            f"{status_icon} {flag} {node.name} - 👥 {node.users_online}"
        )

    servers_list = "\n".join(server_lines) if server_lines else i18n.get("msg-monitoring-no-servers")

    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    return {
        "users_total": str(users_total),
        "users_active": str(users_active),
        "users_disabled": str(users_disabled),
        "users_limited": str(users_limited),
        "users_expired": str(users_expired),
        "online_last_day": str(online_last_day),
        "online_last_week": str(online_last_week),
        "online_never": str(online_never),
        "online_now": str(online_now),
        "total_servers": str(total_servers),
        "available_servers": str(available_servers),
        "total_online": str(total_online),
        "servers_list": servers_list,
        "last_update": now,
    }
