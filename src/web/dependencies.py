"""Shared dependencies for web API routes.

Provides reusable FastAPI Depends for authentication and DI container access.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from dishka import AsyncContainer, Scope
from fastapi import Cookie, HTTPException, Request

from src.core.config import AppConfig
from src.services.user import UserService

from .auth import decode_access_token


def get_secret(request: Request) -> str:
    """Extract crypt_key from app config."""
    config: AppConfig = request.app.state.config
    return config.crypt_key.get_secret_value()


def get_bot_token(request: Request) -> str:
    """Extract bot token from app config."""
    config: AppConfig = request.app.state.config
    return config.bot.token.get_secret_value()


async def get_current_user_id(
    request: Request,
    access_token: Optional[str] = Cookie(default=None),
) -> Optional[int]:
    """Extract telegram_id from JWT cookie. Returns None if not authenticated."""
    if not access_token:
        return None
    payload = decode_access_token(access_token, get_secret(request))
    if payload is None:
        return None
    return payload.get("telegram_id")


async def require_auth(
    request: Request,
    access_token: Optional[str] = Cookie(default=None),
) -> int:
    """Return telegram_id or raise 401."""
    uid = await get_current_user_id(request, access_token)
    if not uid:
        raise HTTPException(status_code=401, detail="Не авторизован")
    return uid


async def require_admin(
    request: Request,
    access_token: Optional[str] = Cookie(default=None),
) -> int:
    """Return telegram_id if user is admin/dev, else raise 401/403."""
    uid = await require_auth(request, access_token)
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        user_service: UserService = await req_container.get(UserService)
        user = await user_service.get(telegram_id=uid)
        if not user or not user.is_privileged:
            raise HTTPException(status_code=403, detail="Недостаточно прав")
    return uid


# ── Brand settings helpers ────────────────────────────────────────

WEB_DIR = Path(__file__).parent
BRAND_FILE = WEB_DIR / "brand_settings.json"
DEFAULT_BRAND: dict[str, str] = {"name": "VPN Shop", "logo": "🔐", "slogan": ""}


def read_brand() -> dict[str, Any]:
    """Read brand settings from JSON file."""
    if BRAND_FILE.exists():
        try:
            return json.loads(BRAND_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return DEFAULT_BRAND.copy()


def write_brand(data: dict[str, Any]) -> None:
    """Write brand settings to JSON file."""
    BRAND_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
