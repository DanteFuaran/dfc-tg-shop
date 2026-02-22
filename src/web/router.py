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

from aiogram import Bot

from src.core.config import AppConfig
from src.core.constants import CONTAINER_KEY
from src.core.enums import UserRole
from src.infrastructure.database import UnitOfWork
from src.infrastructure.database.models.dto.plan import PlanDto
from src.infrastructure.database.models.dto.web_credential import WebCredentialDto
from src.infrastructure.database.models.sql.web_credential import WebCredential
from src.services.plan import PlanService
from src.services.promocode import PromocodeService
from src.services.settings import SettingsService
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

        # Bot username for referral links
        bot_username = ""
        try:
            bot: Bot = await req_container.get(Bot)
            if bot and bot.me:
                bot_username = bot.me.username or ""
        except Exception:
            pass

        # Fetch settings for features & support
        features_data: dict[str, Any] = {}
        support_url = ""
        try:
            settings_service: SettingsService = await req_container.get(SettingsService)
            settings = await settings_service.get()
            features = settings.features
            features_data = {
                "balance_enabled": features.balance_enabled,
                "community_enabled": features.community_enabled,
                "community_url": features.community_url or "",
                "tos_enabled": features.tos_enabled,
                "tos_url": features.tos_url if hasattr(features, "tos_url") else "",
                "referral_enabled": features.referral_enabled,
                "promocodes_enabled": features.promocodes_enabled,
            }
        except Exception:
            pass
        try:
            config: AppConfig = request.app.state.config
            su = config.bot.support_username.get_secret_value() if config.bot.support_username else ""
            if su:
                support_url = f"https://t.me/{su}"
        except Exception:
            pass

        return {
            "user": {
                "telegram_id": user.telegram_id,
                "name": user.name,
                "username": user.username or "",
                "balance": user.balance,
                "role": user.role.value if hasattr(user.role, "value") else str(user.role),
                "language": user.language.value if hasattr(user.language, "value") else str(user.language),
                "is_blocked": user.is_blocked,
            },
            "subscription": sub_data,
            "plans": plans_data,
            "bot_username": bot_username,
            "features": features_data,
            "support_url": support_url,
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

        try:
            pw_hash = hash_password(body.password)
        except Exception as exc:
            logger.error(f"Password hashing failed: {exc}")
            raise HTTPException(status_code=500, detail="Ошибка при создании учётных данных")

        credential = WebCredential(
            telegram_id=body.telegram_id,
            web_username=body.web_username,
            password_hash=pw_hash,
        )
        try:
            await uow.repository.web_credentials.create(credential)
            await uow.commit()
        except Exception as exc:
            logger.error(f"Failed to save web credentials: {exc}")
            raise HTTPException(status_code=500, detail="Ошибка при сохранении учётных данных")

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
# CONFIG API (domain, support, etc.)
# ══════════════════════════════════════════════════════════════════


@router.get("/api/config")
async def api_config(request: Request, access_token: Optional[str] = Cookie(default=None)):
    uid = await _get_current_user_id(request, access_token)
    if not uid:
        raise HTTPException(status_code=401, detail="Не авторизован")
    config: AppConfig = request.app.state.config
    domain = config.domain.get_secret_value() if config.domain else ""
    support_username = ""
    try:
        support_username = config.bot.support_username.get_secret_value() if config.bot.support_username else ""
    except Exception:
        pass
    return JSONResponse({"domain": domain, "support_username": support_username})


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


# ══════════════════════════════════════════════════════════════════
# BRAND SETTINGS
# ══════════════════════════════════════════════════════════════════

BRAND_FILE = WEB_DIR / "brand_settings.json"
DEFAULT_BRAND = {"name": "VPN Shop", "logo": "🔐", "slogan": ""}


def _read_brand() -> dict:
    if BRAND_FILE.exists():
        try:
            return json.loads(BRAND_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return DEFAULT_BRAND.copy()


def _write_brand(data: dict) -> None:
    BRAND_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


@router.get("/api/settings/brand")
async def api_get_brand():
    return JSONResponse(_read_brand())


@router.post("/api/settings/brand")
async def api_set_brand(request: Request, access_token: Optional[str] = Cookie(default=None)):
    uid = await _get_current_user_id(request, access_token)
    if not uid:
        raise HTTPException(status_code=401, detail="Не авторизован")
    # Check admin role
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        user_service: UserService = await req_container.get(UserService)
        user = await user_service.get(telegram_id=uid)
        if not user or not user.is_privileged:
            raise HTTPException(status_code=403, detail="Недостаточно прав")
    body = await request.json()
    brand = _read_brand()
    brand["name"] = body.get("name", brand.get("name", "VPN Shop"))
    brand["logo"] = body.get("logo", brand.get("logo", "🔐"))
    brand["slogan"] = body.get("slogan", brand.get("slogan", ""))
    _write_brand(brand)
    return JSONResponse({"ok": True})


# ══════════════════════════════════════════════════════════════════
# ADMIN HELPER
# ══════════════════════════════════════════════════════════════════


async def _require_admin(request: Request, access_token: Optional[str] = None):
    """Return (telegram_id, UserDto) or raise 401/403."""
    uid = await _get_current_user_id(request, access_token)
    if not uid:
        raise HTTPException(status_code=401, detail="Не авторизован")
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        user_service: UserService = await req_container.get(UserService)
        user = await user_service.get(telegram_id=uid)
        if not user or not user.is_privileged:
            raise HTTPException(status_code=403, detail="Недостаточно прав")
    return uid


# ══════════════════════════════════════════════════════════════════
# ADMIN — STATS
# ══════════════════════════════════════════════════════════════════


@router.get("/api/admin/stats")
async def api_admin_stats(request: Request, access_token: Optional[str] = Cookie(default=None)):
    await _require_admin(request, access_token)
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        user_service: UserService = await req_container.get(UserService)
        subscription_service: SubscriptionService = await req_container.get(SubscriptionService)

        all_users = await user_service.get_all()
        total_users = len(all_users)

        active_subs = 0
        expired_subs = 0
        total_revenue = 0
        for u in all_users:
            total_revenue += u.balance
            sub = await subscription_service.get_current(telegram_id=u.telegram_id)
            if sub:
                status = sub.status.value if hasattr(sub.status, "value") else str(sub.status)
                if status == "ACTIVE":
                    active_subs += 1
                elif status == "EXPIRED":
                    expired_subs += 1

        return JSONResponse({
            "total_users": total_users,
            "active_subscriptions": active_subs,
            "expired_subscriptions": expired_subs,
            "total_revenue": total_revenue,
        })


# ══════════════════════════════════════════════════════════════════
# ADMIN — USERS
# ══════════════════════════════════════════════════════════════════


@router.get("/api/admin/users")
async def api_admin_users(request: Request, access_token: Optional[str] = Cookie(default=None)):
    await _require_admin(request, access_token)
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        user_service: UserService = await req_container.get(UserService)
        users = await user_service.get_all()
        return JSONResponse([
            {
                "telegram_id": u.telegram_id,
                "name": u.name,
                "username": u.username or "",
                "balance": u.balance,
                "role": u.role.value if hasattr(u.role, "value") else str(u.role),
                "is_blocked": u.is_blocked,
            }
            for u in users
        ])


@router.get("/api/admin/users/{tid}")
async def api_admin_user_detail(tid: int, request: Request, access_token: Optional[str] = Cookie(default=None)):
    await _require_admin(request, access_token)
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        user_service: UserService = await req_container.get(UserService)
        subscription_service: SubscriptionService = await req_container.get(SubscriptionService)
        user = await user_service.get(telegram_id=tid)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        sub = await subscription_service.get_current(telegram_id=tid)
        sub_data = None
        if sub:
            sub_data = {
                "status": sub.status.value if hasattr(sub.status, "value") else str(sub.status),
                "plan_name": sub.plan.name if sub.plan else "—",
                "expire_at": sub.expire_at.strftime("%d.%m.%Y %H:%M") if sub.expire_at else "—",
            }

        return JSONResponse({
            "telegram_id": user.telegram_id,
            "name": user.name,
            "username": user.username or "",
            "balance": user.balance,
            "role": user.role.value if hasattr(user.role, "value") else str(user.role),
            "is_blocked": user.is_blocked,
            "created_at": user.created_at.strftime("%d.%m.%Y %H:%M") if user.created_at else "—",
            "subscription": sub_data,
        })


@router.post("/api/admin/users/{tid}/role")
async def api_admin_set_role(tid: int, request: Request, access_token: Optional[str] = Cookie(default=None)):
    await _require_admin(request, access_token)
    body = await request.json()
    role_str = body.get("role", "USER")
    try:
        new_role = UserRole(role_str)
    except (ValueError, KeyError):
        raise HTTPException(status_code=400, detail="Неверная роль")

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        user_service: UserService = await req_container.get(UserService)
        user = await user_service.get(telegram_id=tid)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        await user_service.set_role(user, new_role)
        return JSONResponse({"ok": True})


@router.post("/api/admin/users/{tid}/balance")
async def api_admin_set_balance(tid: int, request: Request, access_token: Optional[str] = Cookie(default=None)):
    await _require_admin(request, access_token)
    body = await request.json()
    amount = body.get("amount", 0)
    if not isinstance(amount, (int, float)):
        raise HTTPException(status_code=400, detail="Неверная сумма")

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        user_service: UserService = await req_container.get(UserService)
        user = await user_service.get(telegram_id=tid)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        user.balance = int(user.balance + amount)
        await user_service.update(user)
        return JSONResponse({"ok": True, "new_balance": user.balance})


@router.post("/api/admin/users/{tid}/block")
async def api_admin_toggle_block(tid: int, request: Request, access_token: Optional[str] = Cookie(default=None)):
    await _require_admin(request, access_token)
    body = await request.json()
    block = body.get("block", True)

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        user_service: UserService = await req_container.get(UserService)
        user = await user_service.get(telegram_id=tid)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        await user_service.set_block(user, block)
        return JSONResponse({"ok": True})


# ══════════════════════════════════════════════════════════════════
# ADMIN — PLANS
# ══════════════════════════════════════════════════════════════════


@router.get("/api/admin/plans")
async def api_admin_plans(request: Request, access_token: Optional[str] = Cookie(default=None)):
    await _require_admin(request, access_token)
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        plan_service: PlanService = await req_container.get(PlanService)
        plans = await plan_service.get_all()
        result = []
        for p in plans:
            durations = []
            for d in (p.durations or []):
                prices = []
                for pr in (d.prices or []):
                    prices.append({
                        "currency": pr.currency.value if hasattr(pr.currency, "value") else str(pr.currency),
                        "amount": str(pr.price),
                    })
                durations.append({"days": d.days, "prices": prices})
            result.append({
                "id": p.id,
                "name": p.name,
                "is_active": p.is_active,
                "traffic_limit": p.traffic_limit,
                "device_limit": p.device_limit,
                "description": p.description or "",
                "durations": durations,
            })
        return JSONResponse(result)


@router.post("/api/admin/plans")
async def api_admin_create_plan(request: Request, access_token: Optional[str] = Cookie(default=None)):
    await _require_admin(request, access_token)
    body = await request.json()
    name = body.get("name", "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="Название обязательно")

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        plan_service: PlanService = await req_container.get(PlanService)
        plan = PlanDto(
            name=name,
            traffic_limit=body.get("traffic_limit", 100),
            device_limit=body.get("device_limit", 1),
            is_active=True,
        )
        created = await plan_service.create(plan)
        return JSONResponse({"ok": True, "id": created.id})


@router.delete("/api/admin/plans/{plan_id}")
async def api_admin_delete_plan(plan_id: int, request: Request, access_token: Optional[str] = Cookie(default=None)):
    await _require_admin(request, access_token)
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        plan_service: PlanService = await req_container.get(PlanService)
        result = await plan_service.delete(plan_id)
        if not result:
            raise HTTPException(status_code=404, detail="Тариф не найден")
        return JSONResponse({"ok": True})


# ══════════════════════════════════════════════════════════════════
# ADMIN — SETTINGS
# ══════════════════════════════════════════════════════════════════


@router.get("/api/admin/settings")
async def api_admin_settings(request: Request, access_token: Optional[str] = Cookie(default=None)):
    await _require_admin(request, access_token)
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        settings_service: SettingsService = await req_container.get(SettingsService)
        settings = await settings_service.get()
        features = settings.features
        return JSONResponse({
            "balance_enabled": features.balance_enabled,
            "community_enabled": features.community_enabled,
            "tos_enabled": features.tos_enabled,
            "referral_enabled": features.referral_enabled,
            "promocodes_enabled": features.promocodes_enabled,
            "notifications_enabled": features.notifications_enabled,
            "access_enabled": features.access_enabled,
            "language_enabled": features.language_enabled,
            "access_mode": settings.access_mode.value if hasattr(settings.access_mode, "value") else str(settings.access_mode),
            "default_currency": settings.default_currency.value if hasattr(settings.default_currency, "value") else str(settings.default_currency),
            "purchases_allowed": settings.purchases_allowed,
            "registration_allowed": settings.registration_allowed,
        })


@router.patch("/api/admin/settings")
async def api_admin_update_settings(request: Request, access_token: Optional[str] = Cookie(default=None)):
    await _require_admin(request, access_token)
    body = await request.json()
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        settings_service: SettingsService = await req_container.get(SettingsService)

        # Toggle feature flags
        feature_fields = {
            "balance_enabled", "community_enabled", "tos_enabled",
            "referral_enabled", "promocodes_enabled", "notifications_enabled",
            "access_enabled", "language_enabled",
        }
        settings_fields = {"purchases_allowed", "registration_allowed"}

        for key, value in body.items():
            if key in feature_fields and isinstance(value, bool):
                await settings_service.toggle_feature(key)
            elif key in settings_fields and isinstance(value, bool):
                settings = await settings_service.get()
                setattr(settings, key, value)
                await settings_service.update(settings)

        return JSONResponse({"ok": True})


# ══════════════════════════════════════════════════════════════════
# PROMOCODE ACTIVATION
# ══════════════════════════════════════════════════════════════════


@router.post("/api/promocode/activate")
async def api_activate_promocode(request: Request, access_token: Optional[str] = Cookie(default=None)):
    uid = await _get_current_user_id(request, access_token)
    if not uid:
        raise HTTPException(status_code=401, detail="Не авторизован")

    body = await request.json()
    code = body.get("code", "").strip()
    if not code:
        raise HTTPException(status_code=400, detail="Введите промокод")

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        promocode_service: PromocodeService = await req_container.get(PromocodeService)
        promo = await promocode_service.get_by_code(code)
        if not promo:
            raise HTTPException(status_code=404, detail="Промокод не найден")
        if not promo.is_active:
            raise HTTPException(status_code=400, detail="Промокод неактивен")
        if promo.max_activations and len(promo.activations or []) >= promo.max_activations:
            raise HTTPException(status_code=400, detail="Промокод исчерпан")
        # Check if user already activated
        for act in (promo.activations or []):
            if act.user_telegram_id == uid:
                raise HTTPException(status_code=400, detail="Вы уже активировали этот промокод")

        return JSONResponse({"message": f"Промокод '{code}' найден. Тип: {promo.reward_type.value if hasattr(promo.reward_type, 'value') else promo.reward_type}. Для полной активации используйте бота."})
