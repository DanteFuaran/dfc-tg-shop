"""Web router — serves Mini App pages and REST API for web cabinet."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from dishka import AsyncContainer, Scope
from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from loguru import logger
from pydantic import BaseModel

from src.core.config import AppConfig
from src.core.constants import CONTAINER_KEY
from src.infrastructure.database import UnitOfWork
from src.infrastructure.database.models.dto.web_credential import WebCredentialDto
from src.infrastructure.database.models.sql.web_credential import WebCredential
from src.services.plan import PlanService
from src.services.subscription import SubscriptionService
from src.services.user import UserService

from .auth import (
    create_access_token,
    decode_access_token,
    hash_password,
    validate_init_data,
    verify_password,
)

WEB_DIR = Path(__file__).parent
TEMPLATES_DIR = WEB_DIR / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter()


# ── Pydantic request models ──────────────────────────────────────


class LoginRequest(BaseModel):
    telegram_id: int


class RegisterRequest(BaseModel):
    telegram_id: int
    web_username: str
    password: str


class PasswordLoginRequest(BaseModel):
    web_username: str
    password: str


# ── Helpers ───────────────────────────────────────────────────────


def _get_secret(request: Request) -> str:
    config: AppConfig = request.app.state.config
    return config.crypt_key.get_secret_value()


def _get_bot_token(request: Request) -> str:
    config: AppConfig = request.app.state.config
    return config.bot.token.get_secret_value()


async def _get_current_user_id(request: Request, access_token: Optional[str] = Cookie(default=None)) -> Optional[int]:
    """Extract telegram_id from JWT cookie. Returns None if not authenticated."""
    if not access_token:
        return None
    payload = decode_access_token(access_token, _get_secret(request))
    if payload is None:
        return None
    return payload.get("telegram_id")


async def _build_user_data(
    request: Request,
    telegram_id: int,
) -> dict[str, Any]:
    """Fetch full user data for dashboard rendering."""
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        user_service: UserService = await req_container.get(UserService)
        subscription_service: SubscriptionService = await req_container.get(SubscriptionService)
        plan_service: PlanService = await req_container.get(PlanService)

        user = await user_service.get(telegram_id=telegram_id)
        if user is None:
            return {}

        subscription = await subscription_service.get_current(telegram_id=telegram_id)
        plans = await plan_service.get_available_plans(user)

        sub_data: dict[str, Any] = {}
        if subscription:
            sub_data = {
                "status": subscription.status.value if hasattr(subscription.status, "value") else str(subscription.status),
                "plan_name": subscription.plan.name if subscription.plan else "—",
                "expire_at": subscription.expire_at.strftime("%d.%m.%Y %H:%M") if subscription.expire_at else "—",
                "traffic_limit": subscription.traffic_limit,
                "device_limit": subscription.device_limit,
                "is_trial": subscription.is_trial,
                "url": subscription.url or "",
            }

        plans_data = []
        for plan in (plans or []):
            durations = []
            for d in (plan.durations or []):
                prices = []
                for p in (d.prices or []):
                    prices.append({
                        "currency": p.currency.value if hasattr(p.currency, "value") else str(p.currency),
                        "amount": str(p.price),
                    })
                durations.append({
                    "days": d.days,
                    "prices": prices,
                })
            plans_data.append({
                "id": plan.id,
                "name": plan.name,
                "traffic_limit": plan.traffic_limit,
                "device_limit": plan.device_limit,
                "durations": durations,
            })

        return {
            "user": {
                "telegram_id": user.telegram_id,
                "name": user.name,
                "username": user.username or "",
                "balance": user.balance,
                "role": user.role.value if hasattr(user.role, "value") else str(user.role),
                "language": user.language.value if hasattr(user.language, "value") else str(user.language),
            },
            "subscription": sub_data,
            "plans": plans_data,
        }


# ══════════════════════════════════════════════════════════════════
# PAGES
# ══════════════════════════════════════════════════════════════════


@router.get("/", response_class=HTMLResponse)
async def web_index(request: Request, access_token: Optional[str] = Cookie(default=None)):
    """Landing — redirect to dashboard if authenticated, else to login."""
    uid = await _get_current_user_id(request, access_token)
    if uid:
        return RedirectResponse(url="/web/dashboard", status_code=302)
    return RedirectResponse(url="/web/login", status_code=302)


@router.get("/login", response_class=HTMLResponse)
async def web_login_page(request: Request):
    config: AppConfig = request.app.state.config
    domain = config.domain.get_secret_value()
    return templates.TemplateResponse("login.html", {"request": request, "domain": domain})


@router.get("/dashboard", response_class=HTMLResponse)
async def web_dashboard_page(request: Request, access_token: Optional[str] = Cookie(default=None)):
    uid = await _get_current_user_id(request, access_token)
    if not uid:
        return RedirectResponse(url="/web/login", status_code=302)

    data = await _build_user_data(request, uid)
    if not data:
        return RedirectResponse(url="/web/login", status_code=302)

    config: AppConfig = request.app.state.config
    domain = config.domain.get_secret_value()

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "data": data, "data_json": json.dumps(data, ensure_ascii=False, default=str), "domain": domain},
    )


@router.get("/miniapp", response_class=HTMLResponse)
async def miniapp_page(request: Request):
    """Telegram Mini App entry point — auth via initData."""
    config: AppConfig = request.app.state.config
    domain = config.domain.get_secret_value()
    return templates.TemplateResponse("miniapp.html", {"request": request, "domain": domain})


# ══════════════════════════════════════════════════════════════════
# AUTH API
# ══════════════════════════════════════════════════════════════════


@router.post("/api/auth/tg")
async def auth_telegram(request: Request):
    """Authenticate via Telegram Mini App initData."""
    body = await request.json()
    init_data = body.get("initData", "")
    bot_token = _get_bot_token(request)

    parsed = validate_init_data(init_data, bot_token)
    if parsed is None:
        raise HTTPException(status_code=401, detail="Invalid initData")

    user_json = parsed.get("user")
    if not user_json:
        raise HTTPException(status_code=401, detail="No user in initData")

    try:
        user_obj = json.loads(user_json)
    except json.JSONDecodeError:
        raise HTTPException(status_code=401, detail="Invalid user JSON")

    telegram_id = user_obj.get("id")
    if not telegram_id:
        raise HTTPException(status_code=401, detail="No user id")

    token = create_access_token(
        {"telegram_id": telegram_id, "source": "miniapp"},
        _get_secret(request),
    )
    response = JSONResponse({"ok": True, "telegram_id": telegram_id})
    response.set_cookie("access_token", token, httponly=True, samesite="none", secure=True, max_age=86400)
    return response


@router.post("/api/auth/check")
async def auth_check_telegram_id(request: Request, body: LoginRequest):
    """Step 1 of web login: check if telegram_id has web credentials."""
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        user_service: UserService = await req_container.get(UserService)

        user = await user_service.get(telegram_id=body.telegram_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь с таким Telegram ID не найден")

        cred = await uow.repository.web_credentials.get_by_telegram_id(body.telegram_id)
        return JSONResponse({
            "has_credentials": cred is not None,
            "name": user.name,
        })


@router.post("/api/auth/register")
async def auth_register(request: Request, body: RegisterRequest):
    """Register web credentials for a telegram user."""
    if len(body.password) < 6:
        raise HTTPException(status_code=400, detail="Пароль должен быть не менее 6 символов")
    if len(body.web_username) < 3:
        raise HTTPException(status_code=400, detail="Логин должен быть не менее 3 символов")

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        user_service: UserService = await req_container.get(UserService)

        user = await user_service.get(telegram_id=body.telegram_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь с таким Telegram ID не найден")

        existing = await uow.repository.web_credentials.get_by_telegram_id(body.telegram_id)
        if existing:
            raise HTTPException(status_code=409, detail="Учётные данные уже существуют")

        username_taken = await uow.repository.web_credentials.get_by_username(body.web_username)
        if username_taken:
            raise HTTPException(status_code=409, detail="Этот логин уже занят")

        credential = WebCredential(
            telegram_id=body.telegram_id,
            web_username=body.web_username,
            password_hash=hash_password(body.password),
        )
        await uow.repository.web_credentials.create(credential)
        await uow.commit()

    token = create_access_token(
        {"telegram_id": body.telegram_id, "source": "web"},
        _get_secret(request),
    )
    response = JSONResponse({"ok": True})
    response.set_cookie("access_token", token, httponly=True, samesite="lax", secure=True, max_age=86400)
    return response


@router.post("/api/auth/login")
async def auth_login(request: Request, body: PasswordLoginRequest):
    """Login with username + password."""
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        uow: UnitOfWork = await req_container.get(UnitOfWork)

        cred = await uow.repository.web_credentials.get_by_username(body.web_username)
        if cred is None:
            raise HTTPException(status_code=401, detail="Неверный логин или пароль")

        if not verify_password(body.password, cred.password_hash):
            raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    token = create_access_token(
        {"telegram_id": cred.telegram_id, "source": "web"},
        _get_secret(request),
    )
    response = JSONResponse({"ok": True})
    response.set_cookie("access_token", token, httponly=True, samesite="lax", secure=True, max_age=86400)
    return response


@router.post("/api/auth/logout")
async def auth_logout():
    response = JSONResponse({"ok": True})
    response.delete_cookie("access_token")
    return response


# ══════════════════════════════════════════════════════════════════
# DATA API
# ══════════════════════════════════════════════════════════════════


@router.get("/api/user/data")
async def api_user_data(request: Request, access_token: Optional[str] = Cookie(default=None)):
    uid = await _get_current_user_id(request, access_token)
    if not uid:
        raise HTTPException(status_code=401, detail="Не авторизован")

    data = await _build_user_data(request, uid)
    if not data:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return JSONResponse(data)


@router.get("/api/user/subscription")
async def api_user_subscription(request: Request, access_token: Optional[str] = Cookie(default=None)):
    uid = await _get_current_user_id(request, access_token)
    if not uid:
        raise HTTPException(status_code=401, detail="Не авторизован")

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        subscription_service: SubscriptionService = await req_container.get(SubscriptionService)
        subscription = await subscription_service.get_current(telegram_id=uid)

        if not subscription:
            return JSONResponse({"subscription": None})

        return JSONResponse({
            "subscription": {
                "status": subscription.status.value if hasattr(subscription.status, "value") else str(subscription.status),
                "plan_name": subscription.plan.name if subscription.plan else "—",
                "expire_at": subscription.expire_at.strftime("%d.%m.%Y %H:%M") if subscription.expire_at else "—",
                "traffic_limit": subscription.traffic_limit,
                "device_limit": subscription.device_limit,
                "is_trial": subscription.is_trial,
                "url": subscription.url or "",
            }
        })
