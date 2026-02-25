"""Admin bot management routes."""

from __future__ import annotations

import os
from pathlib import Path

from dishka import AsyncContainer, Scope
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from src.__version__ import __version__
from src.services.settings import SettingsService
from src.web.dependencies import require_admin

router = APIRouter(prefix="/api/admin/bot", tags=["admin-bot"])

# Known log file paths
_LOG_PATHS = [
    Path("/opt/dfc-tg/logs/bot.log"),
    Path("/opt/dfc-tg-shop/logs/bot.log"),
    Path("/tmp/bot.log"),
]


def _find_log_file() -> Path | None:
    for p in _LOG_PATHS:
        if p.exists():
            return p
    return None


@router.get("/info")
async def api_admin_bot_info(
    request: Request,
    uid: int = Depends(require_admin),
):
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        settings_service: SettingsService = await req_container.get(SettingsService)
        settings = await settings_service.get()

        return JSONResponse({
            "version": __version__,
            "access_mode": settings.access_mode.value if hasattr(settings.access_mode, "value") else str(settings.access_mode),
            "registration_allowed": settings.registration_allowed,
            "purchases_allowed": settings.purchases_allowed,
            "notifications_enabled": settings.notifications_enabled,
            "default_currency": settings.default_currency.value if hasattr(settings.default_currency, "value") else str(settings.default_currency),
            "bot_locale": settings.bot_locale.value if hasattr(settings.bot_locale, "value") else str(settings.bot_locale),
        })


@router.get("/logs")
async def api_admin_bot_logs(
    request: Request,
    uid: int = Depends(require_admin),
    lines: int = 100,
):
    log_path = _find_log_file()
    if not log_path:
        return JSONResponse({"lines": [], "error": "Файл логов не найден"})

    try:
        with open(log_path, "r", encoding="utf-8", errors="replace") as f:
            all_lines = f.readlines()
        last_lines = all_lines[-min(lines, 500):]
        return JSONResponse({"lines": [l.rstrip("\n") for l in last_lines], "path": str(log_path)})
    except Exception as e:
        return JSONResponse({"lines": [], "error": str(e)})
