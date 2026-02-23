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
from src.core.enums import Currency, PlanAvailability, PlanType, PurchaseType, ReferralRewardType, UserRole
from src.infrastructure.database import UnitOfWork
from src.infrastructure.database.models.dto.plan import PlanDto, PlanDurationDto, PlanPriceDto, PlanSnapshotDto
from src.infrastructure.database.models.dto.transaction import PriceDetailsDto
from src.infrastructure.database.models.dto.web_credential import WebCredentialDto
from src.infrastructure.database.models.sql.web_credential import WebCredential
from src.services.payment_gateway import PaymentGatewayService
from src.services.plan import PlanService
from src.services.pricing import PricingService
from src.services.promocode import PromocodeService
from src.services.referral import ReferralService
from src.services.remnawave import RemnawaveService
from src.services.settings import SettingsService
from src.services.subscription import SubscriptionService
from src.services.ticket import TicketService
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
        active_devices_count = 0
        if subscription:
            sub_data = {
                "status": subscription.status.value if hasattr(subscription.status, "value") else str(subscription.status),
                "plan_name": subscription.plan.name if subscription.plan else "—",
                "plan_id": subscription.plan.id if subscription.plan else None,
                "expire_at": subscription.expire_at.strftime("%d.%m.%Y %H:%M") if subscription.expire_at else "—",
                "traffic_limit": subscription.traffic_limit,
                "device_limit": subscription.device_limit,
                "is_trial": subscription.is_trial,
                "url": subscription.url or "",
            }
            try:
                remnawave_svc: RemnawaveService = await req_container.get(RemnawaveService)
                devices = await remnawave_svc.get_devices_user(user=user)
                active_devices_count = len(devices) if devices else 0
            except Exception:
                active_devices_count = 0
            sub_data["active_devices_count"] = active_devices_count

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
                "description": plan.description or "" if hasattr(plan, 'description') else "",
                "type": plan.type.value if hasattr(plan, 'type') and plan.type else "BOTH",
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
        default_currency = "RUB"
        bot_locale = "RU"
        try:
            settings_service: SettingsService = await req_container.get(SettingsService)
            settings = await settings_service.get()
            features = settings.features
            default_currency = settings.default_currency.value if hasattr(settings.default_currency, "value") else str(settings.default_currency)
            bot_locale = settings.bot_locale.value if hasattr(settings.bot_locale, "value") else str(settings.bot_locale)
            features_data = {
                "balance_enabled": features.balance_enabled,
                "balance_mode": features.balance_mode.value if hasattr(features.balance_mode, "value") else str(features.balance_mode),
                "community_enabled": features.community_enabled,
                "community_url": features.community_url or "",
                "tos_enabled": features.tos_enabled,
                "tos_url": features.tos_url if hasattr(features, "tos_url") else "",
                "referral_enabled": features.referral_enabled,
                "promocodes_enabled": features.promocodes_enabled,
            }
        except Exception:
            pass

        # Referral balance for profile display
        referral_balance_user = 0
        try:
            ref_svc: ReferralService = await req_container.get(ReferralService)
            referral_balance_user = await ref_svc.get_pending_rewards_amount(telegram_id=telegram_id, reward_type=ReferralRewardType.MONEY)
        except Exception:
            pass
        try:
            config: AppConfig = request.app.state.config
            su = config.bot.support_username.get_secret_value() if config.bot.support_username else ""
            if su:
                support_url = f"https://t.me/{su}"
        except Exception:
            pass

        # Trial availability check — hide if user used trial OR has/had any subscription
        trial_available = False
        try:
            has_used = await subscription_service.has_used_trial(telegram_id)
            has_any_sub = sub_data is not None  # user has current subscription
            if not has_any_sub:
                # Also check if user ever had any subscription
                all_subs = await subscription_service.get_all_by_user(telegram_id)
                has_any_sub = len(all_subs) > 0
            if not has_used and not has_any_sub:
                trial_plan = await plan_service.get_trial_plan()
                if trial_plan and trial_plan.is_active:
                    trial_available = True
        except Exception:
            pass

        # Ticket unread count
        ticket_unread = 0
        has_open_tickets = False
        try:
            ticket_svc: TicketService = await req_container.get(TicketService)
            uow_t: UnitOfWork = await req_container.get(UnitOfWork)
            ticket_unread = await ticket_svc.count_unread_user(uow_t, telegram_id)
            user_tickets = await ticket_svc.get_user_tickets(uow_t, telegram_id)
            has_open_tickets = any(t.status != "CLOSED" and t.status.value != "CLOSED" if hasattr(t.status, 'value') else t.status != "CLOSED" for t in user_tickets) if user_tickets else False
        except Exception:
            pass

        return {
            "user": {
                "telegram_id": user.telegram_id,
                "name": user.name,
                "username": user.username or "",
                "balance": user.balance,
                "referral_balance": referral_balance_user,
                "referral_code": user.referral_code if hasattr(user, 'referral_code') else "",
                "role": user.role.value if hasattr(user.role, "value") else str(user.role),
                "language": user.language.value if hasattr(user.language, "value") else str(user.language),
                "is_blocked": user.is_blocked,
            },
            "subscription": sub_data,
            "plans": plans_data,
            "bot_username": bot_username,
            "features": features_data,
            "support_url": support_url,
            "trial_available": trial_available,
            "default_currency": default_currency,
            "bot_locale": bot_locale,
            "ticket_unread": ticket_unread,
            "has_open_tickets": has_open_tickets,
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

    config: AppConfig = request.app.state.config
    domain = config.domain.get_secret_value()

    return templates.TemplateResponse(
        "miniapp.html",
        {"request": request, "domain": domain},
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


@router.get("/api/tickets/status")
async def api_tickets_status(request: Request, access_token: Optional[str] = Cookie(default=None)):
    """Lightweight endpoint for polling ticket status (FAB badge)."""
    uid = await _get_current_user_id(request, access_token)
    if not uid:
        raise HTTPException(status_code=401, detail="Не авторизован")

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        unread = await ticket_svc.count_unread_user(uow, uid)
        user_tickets = await ticket_svc.get_user_tickets(uow, uid)
        has_open = any(
            t.status != "CLOSED" and (t.status.value != "CLOSED" if hasattr(t.status, 'value') else True)
            for t in user_tickets
        ) if user_tickets else False
        result = {"has_open": has_open, "unread": unread}
        # If admin, also return admin unread count
        try:
            user_service: UserService = await req_container.get(UserService)
            user = await user_service.get(telegram_id=uid)
            if user and user.is_privileged:
                uow2: UnitOfWork = await req_container.get(UnitOfWork)
                admin_unread = await ticket_svc.count_unread_admin(uow2)
                result["admin_unread"] = admin_unread
        except Exception:
            pass
        return JSONResponse(result)


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
                "plan_id": subscription.plan.id if subscription.plan else None,
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

        referral_balance = 0
        try:
            referral_service: ReferralService = await req_container.get(ReferralService)
            referral_balance = await referral_service.get_pending_rewards_amount(telegram_id=tid, reward_type=ReferralRewardType.MONEY)
        except Exception:
            pass

        return JSONResponse({
            "telegram_id": user.telegram_id,
            "name": user.name,
            "username": user.username or "",
            "balance": user.balance,
            "referral_balance": referral_balance,
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


@router.post("/api/admin/users/{tid}/bonus-balance")
async def api_admin_set_bonus_balance(tid: int, request: Request, access_token: Optional[str] = Cookie(default=None)):
    """Admin: modify user bonus balance via referral rewards."""
    await _require_admin(request, access_token)
    body = await request.json()
    amount = body.get("amount", 0)
    if not isinstance(amount, (int, float)):
        raise HTTPException(status_code=400, detail="Неверная сумма")

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        user_service: UserService = await req_container.get(UserService)
        referral_service: ReferralService = await req_container.get(ReferralService)
        user = await user_service.get(telegram_id=tid)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        # Create a direct reward in the bonus (referral) balance, not main balance
        await referral_service.create_direct_reward(
            user_telegram_id=tid,
            amount=int(amount),
            reward_type=ReferralRewardType.MONEY,
        )
        # Return updated bonus balance
        new_bonus = await referral_service.get_pending_rewards_amount(
            telegram_id=tid, reward_type=ReferralRewardType.MONEY,
        )
        return JSONResponse({"ok": True, "new_balance": new_bonus})


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
                durations.append({"id": d.id, "days": d.days, "prices": prices})
            result.append({
                "id": p.id,
                "name": p.name,
                "is_active": p.is_active,
                "type": p.type.value if hasattr(p.type, "value") else str(p.type),
                "availability": p.availability.value if hasattr(p.availability, "value") else str(p.availability),
                "traffic_limit": p.traffic_limit,
                "device_limit": p.device_limit,
                "description": p.description or "",
                "tag": p.tag or "",
                "order_index": p.order_index,
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

        # Parse availability
        avail_str = body.get("availability", "ALL")
        try:
            availability = PlanAvailability(avail_str)
        except (ValueError, KeyError):
            availability = PlanAvailability.ALL

        # Parse type
        type_str = body.get("type", "BOTH")
        try:
            plan_type = PlanType(type_str)
        except (ValueError, KeyError):
            plan_type = PlanType.BOTH

        # Parse durations
        durations = []
        for dur_data in body.get("durations", []):
            prices = []
            for price_data in dur_data.get("prices", []):
                try:
                    currency = Currency(price_data.get("currency", "RUB"))
                except (ValueError, KeyError):
                    currency = Currency.RUB
                from decimal import Decimal
                prices.append(PlanPriceDto(
                    currency=currency,
                    price=Decimal(str(price_data.get("amount", "0"))),
                ))
            durations.append(PlanDurationDto(
                days=int(dur_data.get("days", 30)),
                prices=prices,
            ))

        plan = PlanDto(
            name=name,
            description=body.get("description", "").strip() or None,
            tag=body.get("tag", "").strip() or None,
            traffic_limit=body.get("traffic_limit", 100),
            device_limit=body.get("device_limit", 1),
            is_active=body.get("is_active", True),
            type=plan_type,
            availability=availability,
            durations=durations,
        )
        created = await plan_service.create(plan)
        return JSONResponse({"ok": True, "id": created.id})


@router.put("/api/admin/plans/{plan_id}")
async def api_admin_update_plan(plan_id: int, request: Request, access_token: Optional[str] = Cookie(default=None)):
    await _require_admin(request, access_token)
    body = await request.json()

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        plan_service: PlanService = await req_container.get(PlanService)
        existing = await plan_service.get(plan_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Тариф не найден")

        # Update fields if provided
        if "name" in body:
            existing.name = body["name"].strip() or existing.name
        if "description" in body:
            existing.description = body["description"].strip() or None
        if "tag" in body:
            existing.tag = body["tag"].strip() or None
        if "traffic_limit" in body:
            existing.traffic_limit = int(body["traffic_limit"])
        if "device_limit" in body:
            existing.device_limit = int(body["device_limit"])
        if "is_active" in body:
            existing.is_active = bool(body["is_active"])

        if "availability" in body:
            try:
                existing.availability = PlanAvailability(body["availability"])
            except (ValueError, KeyError):
                pass
        if "type" in body:
            try:
                existing.type = PlanType(body["type"])
            except (ValueError, KeyError):
                pass

        # Update durations if provided
        if "durations" in body:
            durations = []
            for dur_data in body["durations"]:
                prices = []
                for price_data in dur_data.get("prices", []):
                    try:
                        currency = Currency(price_data.get("currency", "RUB"))
                    except (ValueError, KeyError):
                        currency = Currency.RUB
                    from decimal import Decimal
                    prices.append(PlanPriceDto(
                        currency=currency,
                        price=Decimal(str(price_data.get("amount", "0"))),
                    ))
                durations.append(PlanDurationDto(
                    days=int(dur_data.get("days", 30)),
                    prices=prices,
                ))
            existing.durations = durations

        updated = await plan_service.update(existing)
        if not updated:
            raise HTTPException(status_code=500, detail="Ошибка обновления тарифа")
        return JSONResponse({"ok": True})


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


@router.patch("/api/admin/plans/{plan_id}/toggle")
async def api_admin_toggle_plan(plan_id: int, request: Request, access_token: Optional[str] = Cookie(default=None)):
    """Toggle is_active for a plan."""
    await _require_admin(request, access_token)
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        plan_service: PlanService = await req_container.get(PlanService)
        plan = await plan_service.get(plan_id)
        if not plan:
            raise HTTPException(status_code=404, detail="Тариф не найден")
        plan.is_active = not plan.is_active
        updated = await plan_service.update(plan)
        if not updated:
            raise HTTPException(status_code=500, detail="Ошибка обновления")
        return JSONResponse({"ok": True, "is_active": plan.is_active})


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
        ed = features.extra_devices
        tr = features.transfers
        inot = features.inactive_notifications
        gd = features.global_discount
        cr = features.currency_rates
        ref = settings.referral
        u_notif = settings.user_notifications
        s_notif = settings.system_notifications
        return JSONResponse({
            "balance_enabled": features.balance_enabled,
            "balance_mode": features.balance_mode.value if hasattr(features.balance_mode, "value") else str(features.balance_mode),
            "balance_min_amount": features.balance_min_amount,
            "balance_max_amount": features.balance_max_amount,
            "community_enabled": features.community_enabled,
            "community_url": features.community_url or "",
            "tos_enabled": features.tos_enabled,
            "referral_enabled": features.referral_enabled,
            "referral_level": ref.level.value if hasattr(ref.level, "value") else str(ref.level),
            "referral_accrual_strategy": ref.accrual_strategy.value if hasattr(ref.accrual_strategy, "value") else str(ref.accrual_strategy),
            "referral_reward_type": ref.reward.type.value if hasattr(ref.reward.type, "value") else str(ref.reward.type),
            "referral_reward_strategy": ref.reward.strategy.value if hasattr(ref.reward.strategy, "value") else str(ref.reward.strategy),
            "referral_reward_value": ref.reward.config.get(ref.level, 10),
            "referral_invite_message": ref.invite_message or "",
            "promocodes_enabled": features.promocodes_enabled,
            "notifications_enabled": features.notifications_enabled,
            "extra_devices_enabled": ed.enabled,
            "extra_devices_price": ed.price_per_device,
            "extra_devices_one_time": ed.is_one_time,
            "extra_devices_min_days": ed.min_days,
            "transfers_enabled": tr.enabled,
            "transfers_commission_type": tr.commission_type,
            "transfers_commission_value": tr.commission_value,
            "transfers_min_amount": tr.min_amount,
            "transfers_max_amount": tr.max_amount,
            "inactive_notif_enabled": inot.enabled,
            "inactive_notif_hours": inot.hours_threshold,
            "global_discount_enabled": gd.enabled,
            "global_discount_type": gd.discount_type,
            "global_discount_value": gd.discount_value,
            "global_discount_stack": gd.stack_discounts,
            "global_discount_apply_sub": gd.apply_to_subscription,
            "global_discount_apply_devices": gd.apply_to_extra_devices,
            "global_discount_apply_transfer": gd.apply_to_transfer_commission,
            "currency_rates_auto": cr.auto_update,
            "currency_rates_usd": cr.usd_rate,
            "currency_rates_eur": cr.eur_rate,
            "currency_rates_stars": cr.stars_rate,
            "access_enabled": features.access_enabled,
            "language_enabled": features.language_enabled,
            "access_mode": settings.access_mode.value if hasattr(settings.access_mode, "value") else str(settings.access_mode),
            "default_currency": settings.default_currency.value if hasattr(settings.default_currency, "value") else str(settings.default_currency),
            "purchases_allowed": settings.purchases_allowed,
            "registration_allowed": settings.registration_allowed,
            "rules_required": settings.rules_required,
            "channel_required": settings.channel_required,
            "channel_link": settings.channel_link.get_secret_value() if hasattr(settings.channel_link, "get_secret_value") else str(settings.channel_link),
            "tos_url": settings.rules_link.get_secret_value() if hasattr(settings.rules_link, "get_secret_value") else str(settings.rules_link),
            "bot_locale": settings.bot_locale.value if hasattr(settings.bot_locale, "value") else str(settings.bot_locale),
            # User notifications
            "un_expires_3d": u_notif.expires_in_3_days,
            "un_expires_2d": u_notif.expires_in_2_days,
            "un_expires_1d": u_notif.expires_in_1_days,
            "un_expired": u_notif.expired,
            "un_limited": u_notif.limited,
            "un_expired_1d_ago": u_notif.expired_1_day_ago,
            "un_referral_attached": u_notif.referral_attached,
            "un_referral_reward": u_notif.referral_reward,
            # System notifications
            "sn_bot_lifetime": s_notif.bot_lifetime,
            "sn_bot_update": s_notif.bot_update,
            "sn_user_registered": s_notif.user_registered,
            "sn_subscription": s_notif.subscription,
            "sn_extra_devices": s_notif.extra_devices,
            "sn_promocode": s_notif.promocode_activated,
            "sn_trial": s_notif.trial_getted,
            "sn_node_status": s_notif.node_status,
            "sn_user_connected": s_notif.user_first_connected,
            "sn_user_hwid": s_notif.user_hwid,
            "sn_billing": s_notif.billing,
            "sn_balance_transfer": s_notif.balance_transfer,
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
        settings_fields = {"purchases_allowed", "registration_allowed", "channel_required"}
        settings_bool_fields = {"rules_required"}
        settings_str_fields = {"tos_url", "channel_link"}
        string_feature_fields = {"community_url"}

        # Sub-settings mapping: key -> (parent_attr, child_attr, type)
        sub_settings_map = {
            "balance_mode": ("features", "balance_mode", "balance_mode"),
            "balance_min_amount": ("features", "balance_min_amount", "int_or_none"),
            "balance_max_amount": ("features", "balance_max_amount", "int_or_none"),
            "extra_devices_enabled": ("features.extra_devices", "enabled", "bool"),
            "extra_devices_price": ("features.extra_devices", "price_per_device", "int"),
            "extra_devices_one_time": ("features.extra_devices", "is_one_time", "bool"),
            "extra_devices_min_days": ("features.extra_devices", "min_days", "int"),
            "transfers_enabled": ("features.transfers", "enabled", "bool"),
            "transfers_commission_type": ("features.transfers", "commission_type", "str"),
            "transfers_commission_value": ("features.transfers", "commission_value", "int"),
            "transfers_min_amount": ("features.transfers", "min_amount", "int"),
            "transfers_max_amount": ("features.transfers", "max_amount", "int"),
            "inactive_notif_enabled": ("features.inactive_notifications", "enabled", "bool"),
            "inactive_notif_hours": ("features.inactive_notifications", "hours_threshold", "int"),
            "global_discount_enabled": ("features.global_discount", "enabled", "bool"),
            "global_discount_type": ("features.global_discount", "discount_type", "str"),
            "global_discount_value": ("features.global_discount", "discount_value", "int"),
            "global_discount_stack": ("features.global_discount", "stack_discounts", "bool"),
            "global_discount_apply_sub": ("features.global_discount", "apply_to_subscription", "bool"),
            "global_discount_apply_devices": ("features.global_discount", "apply_to_extra_devices", "bool"),
            "global_discount_apply_transfer": ("features.global_discount", "apply_to_transfer_commission", "bool"),
            "currency_rates_auto": ("features.currency_rates", "auto_update", "bool"),
            "currency_rates_usd": ("features.currency_rates", "usd_rate", "float"),
            "currency_rates_eur": ("features.currency_rates", "eur_rate", "float"),
            "currency_rates_stars": ("features.currency_rates", "stars_rate", "float"),
        }

        settings = await settings_service.get()
        need_save = False

        for key, value in body.items():
            if key in feature_fields and isinstance(value, bool):
                await settings_service.toggle_feature(key)
            elif key in settings_bool_fields and isinstance(value, bool):
                settings = await settings_service.get()
                setattr(settings, key, value)
                need_save = True
            elif key in settings_str_fields and isinstance(value, str):
                settings = await settings_service.get()
                if key == "tos_url":
                    from pydantic import SecretStr
                    settings.rules_link = SecretStr(value)
                elif key == "channel_link":
                    from pydantic import SecretStr
                    settings.channel_link = SecretStr(value)
                need_save = True
            elif key in settings_fields and isinstance(value, bool):
                settings = await settings_service.get()
                setattr(settings, key, value)
                need_save = True
            elif key in string_feature_fields and isinstance(value, str):
                settings = await settings_service.get()
                setattr(settings.features, key, value)
                need_save = True
            elif key in sub_settings_map:
                parent_path, attr, val_type = sub_settings_map[key]
                # Navigate to parent object
                obj = settings
                for part in parent_path.split("."):
                    obj = getattr(obj, part)
                # Convert and set value
                if val_type == "bool":
                    setattr(obj, attr, bool(value))
                elif val_type == "int":
                    setattr(obj, attr, int(value))
                elif val_type == "int_or_none":
                    setattr(obj, attr, int(value) if value is not None else None)
                elif val_type == "float":
                    setattr(obj, attr, float(value))
                elif val_type == "str":
                    setattr(obj, attr, str(value))
                elif val_type == "balance_mode":
                    from src.core.enums import BalanceMode
                    setattr(obj, attr, BalanceMode(str(value)))
                need_save = True
            # Referral settings
            elif key == "referral_level":
                from src.core.enums import ReferralLevel
                settings.referral.level = ReferralLevel(int(value))
                need_save = True
            elif key == "referral_accrual_strategy":
                from src.core.enums import ReferralAccrualStrategy
                settings.referral.accrual_strategy = ReferralAccrualStrategy(str(value))
                need_save = True
            elif key == "referral_reward_type":
                from src.core.enums import ReferralRewardType
                settings.referral.reward.type = ReferralRewardType(str(value))
                need_save = True
            elif key == "referral_reward_strategy":
                from src.core.enums import ReferralRewardStrategy
                settings.referral.reward.strategy = ReferralRewardStrategy(str(value))
                need_save = True
            elif key == "referral_reward_value":
                settings.referral.reward.config[settings.referral.level] = int(value)
                need_save = True
            elif key == "referral_invite_message":
                settings.referral.invite_message = str(value)
                need_save = True
            # User notifications
            elif key.startswith("un_"):
                field = key[3:]
                if hasattr(settings.user_notifications, field):
                    setattr(settings.user_notifications, field, bool(value))
                    need_save = True
            # System notifications
            elif key.startswith("sn_"):
                field = key[3:]
                if hasattr(settings.system_notifications, field):
                    setattr(settings.system_notifications, field, bool(value))
                    need_save = True

        if need_save:
            await settings_service.update(settings)

        return JSONResponse({"ok": True})


# ══════════════════════════════════════════════════════════════════
# ADMIN — PAYMENT GATEWAYS
# ══════════════════════════════════════════════════════════════════


@router.get("/api/admin/gateways")
async def api_admin_gateways(request: Request, access_token: Optional[str] = Cookie(default=None)):
    """Return all payment gateways (for admin settings)."""
    await _require_admin(request, access_token)
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        gw_service: PaymentGatewayService = await req_container.get(PaymentGatewayService)
        gateways = await gw_service.get_all(order_by_priority=True)
        result = []
        for gw in gateways:
            item: dict[str, Any] = {
                "id": gw.id,
                "type": gw.type.value if hasattr(gw.type, "value") else str(gw.type),
                "is_active": gw.is_active,
                "currency": gw.currency.value if hasattr(gw.currency, "value") else str(gw.currency),
                "order_index": gw.order_index,
            }
            # Include settings fields (hide secret values, show only whether they are set)
            if gw.settings:
                settings_data: dict[str, Any] = {}
                for field_name, field_value in gw.settings.__dict__.items():
                    if field_name == "type":
                        continue
                    from pydantic import SecretStr
                    if isinstance(field_value, SecretStr):
                        settings_data[field_name] = field_value.get_secret_value() if field_value else ""
                    else:
                        val = field_value
                        if hasattr(val, "value"):
                            val = val.value
                        settings_data[field_name] = val if val is not None else ""
                item["settings"] = settings_data
            else:
                item["settings"] = {}
            result.append(item)
        return JSONResponse(result)


@router.patch("/api/admin/gateways/{gateway_id}")
async def api_admin_update_gateway(gateway_id: int, request: Request, access_token: Optional[str] = Cookie(default=None)):
    """Update a payment gateway (toggle is_active, update settings fields)."""
    await _require_admin(request, access_token)
    body = await request.json()
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        gw_service: PaymentGatewayService = await req_container.get(PaymentGatewayService)
        gw = await gw_service.get(gateway_id)
        if not gw:
            raise HTTPException(status_code=404, detail="Платёжная система не найдена")

        # Toggle is_active
        if "is_active" in body:
            gw.is_active = bool(body["is_active"])

        # Update settings fields
        if "settings" in body and isinstance(body["settings"], dict) and gw.settings:
            from pydantic import SecretStr
            for field_name, field_value in body["settings"].items():
                if field_name == "type":
                    continue
                if hasattr(gw.settings, field_name):
                    field_info = gw.settings.model_fields.get(field_name)
                    if field_info and field_info.annotation in (
                        Optional[SecretStr], SecretStr
                    ):
                        setattr(gw.settings, field_name, SecretStr(str(field_value)) if field_value else None)
                    else:
                        setattr(gw.settings, field_name, field_value if field_value != "" else None)

        updated = await gw_service.update(gw)
        if not updated:
            raise HTTPException(status_code=500, detail="Ошибка обновления")
        return JSONResponse({"ok": True})


# ══════════════════════════════════════════════════════════════════
# PURCHASE & TRIAL
# ══════════════════════════════════════════════════════════════════


@router.post("/api/purchase")
async def api_purchase(request: Request, access_token: Optional[str] = Cookie(default=None)):
    """User: purchase a plan with balance."""
    uid = await _get_current_user_id(request, access_token)
    if not uid:
        raise HTTPException(status_code=401, detail="Не авторизован")

    body = await request.json()
    plan_id = body.get("plan_id")
    duration_days = body.get("duration_days")
    if not plan_id or not duration_days:
        raise HTTPException(status_code=400, detail="Укажите plan_id и duration_days")

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        user_service: UserService = await req_container.get(UserService)
        plan_service: PlanService = await req_container.get(PlanService)
        payment_gw: PaymentGatewayService = await req_container.get(PaymentGatewayService)
        settings_service: SettingsService = await req_container.get(SettingsService)
        pricing_service: PricingService = await req_container.get(PricingService)
        referral_service: ReferralService = await req_container.get(ReferralService)
        subscription_service: SubscriptionService = await req_container.get(SubscriptionService)

        user = await user_service.get(telegram_id=uid)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        plan = await plan_service.get(plan_id)
        if not plan or not plan.is_active:
            raise HTTPException(status_code=404, detail="Тариф не найден")

        duration = plan.get_duration(duration_days)
        if not duration:
            raise HTTPException(status_code=400, detail="Период не найден")

        settings = await settings_service.get()
        currency = settings.default_currency

        price_obj = duration.get_price(currency)
        if not price_obj:
            raise HTTPException(status_code=400, detail="Цена не найдена")

        from decimal import Decimal
        base_price = Decimal(str(price_obj))

        global_discount = settings.features.global_discount if hasattr(settings.features, 'global_discount') else None
        price = pricing_service.calculate(user, base_price, currency, global_discount, context="subscription")

        # Check balance (with combined mode support)
        is_combined = await settings_service.is_balance_combined()
        referral_balance = await referral_service.get_pending_rewards_amount(
            telegram_id=uid, reward_type=ReferralRewardType.MONEY,
        )
        available = user.balance + referral_balance if is_combined else user.balance

        if available < price.final_amount:
            raise HTTPException(status_code=400, detail="Недостаточно средств")

        # Determine purchase type
        current_sub = await subscription_service.get_current(telegram_id=uid)
        if current_sub and current_sub.status in ["ACTIVE", "active"]:
            # Trial/referral → treat as NEW (full plan update in Remnawave)
            if current_sub.is_trial or (current_sub.plan and current_sub.plan.name and any(
                kw in current_sub.plan.name.lower() for kw in ("пробн", "trial", "реферал", "referral")
            )):
                purchase_type = PurchaseType.NEW
            else:
                purchase_type = PurchaseType.RENEW
        else:
            purchase_type = PurchaseType.NEW

        plan_snapshot = PlanSnapshotDto.from_plan(plan, duration_days)

        try:
            result = await payment_gw.create_balance_payment(
                user=user, plan=plan_snapshot, pricing=price, purchase_type=purchase_type,
            )

            from_main, from_bonus = await user_service.subtract_from_combined_balance(
                user=user, amount=int(price.final_amount),
                referral_balance=referral_balance, is_combined=is_combined,
            )

            if from_bonus > 0:
                await referral_service.withdraw_pending_rewards(
                    telegram_id=uid, reward_type=ReferralRewardType.MONEY, amount=from_bonus,
                )

            await payment_gw.handle_payment_succeeded(result.id, run_sync=True)
            return JSONResponse({"ok": True})

        except Exception as e:
            logger.exception(f"Purchase failed for user {uid}: {e}")
            raise HTTPException(status_code=500, detail="Ошибка обработки покупки")


@router.post("/api/trial/activate")
async def api_trial_activate(request: Request, access_token: Optional[str] = Cookie(default=None)):
    """User: activate trial subscription."""
    uid = await _get_current_user_id(request, access_token)
    if not uid:
        raise HTTPException(status_code=401, detail="Не авторизован")

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        user_service: UserService = await req_container.get(UserService)
        plan_service: PlanService = await req_container.get(PlanService)
        subscription_service: SubscriptionService = await req_container.get(SubscriptionService)
        remnawave_service: RemnawaveService = await req_container.get(RemnawaveService)

        user = await user_service.get(telegram_id=uid)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        # Check if trial already used
        has_used = await subscription_service.has_used_trial(uid)
        if has_used:
            raise HTTPException(status_code=400, detail="Пробная подписка уже использована")

        # Get trial plan
        trial_plan = await plan_service.get_trial_plan()
        if not trial_plan or not trial_plan.is_active:
            raise HTTPException(status_code=400, detail="Пробная подписка недоступна")

        trial_snapshot = PlanSnapshotDto.from_plan(trial_plan, trial_plan.durations[0].days)

        try:
            from src.infrastructure.database.models.dto.subscription import SubscriptionDto

            # Create user in Remnawave
            created_remna_user = await remnawave_service.create_user(user, plan=trial_snapshot, force=True)

            trial_subscription = SubscriptionDto(
                user_remna_id=created_remna_user.uuid,
                status=created_remna_user.status,
                is_trial=True,
                traffic_limit=trial_snapshot.traffic_limit,
                device_limit=trial_snapshot.device_limit,
                traffic_limit_strategy=trial_snapshot.traffic_limit_strategy,
                tag=trial_snapshot.tag,
                internal_squads=trial_snapshot.internal_squads,
                external_squad=trial_snapshot.external_squad,
                expire_at=created_remna_user.expire_at,
                url=created_remna_user.subscription_url,
                plan=trial_snapshot,
            )

            await subscription_service.create(user, trial_subscription)
            await user_service.clear_user_cache(uid)

            return JSONResponse({"ok": True})

        except Exception as e:
            logger.exception(f"Trial activation failed for user {uid}: {e}")
            raise HTTPException(status_code=500, detail="Ошибка активации пробной подписки")


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


# ══════════════════════════════════════════════════════════════════
# TICKETS  (Support ticket system)
# ══════════════════════════════════════════════════════════════════


def _ticket_to_dict(t) -> dict[str, Any]:
    """Convert TicketDto to JSON-serialisable dict."""
    return {
        "id": t.id,
        "subject": t.subject,
        "status": t.status.value if hasattr(t.status, "value") else str(t.status),
        "user_telegram_id": t.user_telegram_id,
        "is_read_by_user": t.is_read_by_user,
        "is_read_by_admin": t.is_read_by_admin,
        "created_at": t.created_at.strftime("%d.%m.%Y %H:%M") if t.created_at else "",
        "updated_at": t.updated_at.strftime("%d.%m.%Y %H:%M") if t.updated_at else "",
        "messages": [
            {
                "id": m.id,
                "is_admin": m.is_admin,
                "text": m.text,
                "created_at": m.created_at.strftime("%d.%m.%Y %H:%M") if m.created_at else "",
            }
            for m in (t.messages or [])
        ],
    }


@router.get("/api/tickets")
async def api_get_tickets(request: Request, access_token: Optional[str] = Cookie(default=None)):
    """User: get own tickets."""
    uid = await _get_current_user_id(request, access_token)
    if not uid:
        raise HTTPException(status_code=401, detail="Не авторизован")

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        tickets = await ticket_svc.get_user_tickets(uow, uid)
        return JSONResponse([_ticket_to_dict(t) for t in tickets])


@router.post("/api/tickets")
async def api_create_ticket(request: Request, access_token: Optional[str] = Cookie(default=None)):
    """User: create a new ticket."""
    uid = await _get_current_user_id(request, access_token)
    if not uid:
        raise HTTPException(status_code=401, detail="Не авторизован")

    body = await request.json()
    subject = (body.get("subject") or "").strip()
    text = (body.get("text") or "").strip()
    if not subject or not text:
        raise HTTPException(status_code=400, detail="Заполните тему и сообщение")

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        ticket = await ticket_svc.create_ticket(uow, uid, subject, text)

        # Notify admins/devs via bot (with close button, no auto-delete)
        try:
            from src.services.notification import NotificationService
            from src.core.utils.message_payload import MessagePayload
            from src.core.enums import UserRole
            ntf: NotificationService = await req_container.get(NotificationService)
            user_service: UserService = await req_container.get(UserService)
            user = await user_service.get(telegram_id=uid)
            user_label = f"{user.name} (@{user.username})" if user and user.username else (user.name if user else str(uid))
            ticket_text = f"🎫 Новый тикет #{ticket.id}\n\n👤 {user_label}\n📝 {subject}\n\n{text[:300]}"
            payload = MessagePayload.not_deleted(text=ticket_text)
            # Send to all DEV and ADMIN users
            devs = await user_service.get_by_role(role=UserRole.DEV)
            admins = await user_service.get_by_role(role=UserRole.ADMIN)
            recipients = {u.telegram_id: u for u in (devs or []) + (admins or [])}
            for recipient in recipients.values():
                try:
                    await ntf.notify_user(user=recipient, payload=payload)
                except Exception:
                    pass
        except Exception:
            pass

        return JSONResponse(_ticket_to_dict(ticket))


@router.get("/api/tickets/{ticket_id}")
async def api_get_ticket(ticket_id: int, request: Request, access_token: Optional[str] = Cookie(default=None)):
    """User: get ticket detail. Mark as read."""
    uid = await _get_current_user_id(request, access_token)
    if not uid:
        raise HTTPException(status_code=401, detail="Не авторизован")

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        ticket = await ticket_svc.get_ticket(uow, ticket_id)
        if not ticket or ticket.user_telegram_id != uid:
            raise HTTPException(status_code=404, detail="Тикет не найден")
        await ticket_svc.mark_read_by_user(uow, ticket_id)
        return JSONResponse(_ticket_to_dict(ticket))


@router.post("/api/tickets/{ticket_id}/reply")
async def api_reply_ticket(ticket_id: int, request: Request, access_token: Optional[str] = Cookie(default=None)):
    """User: reply to own ticket."""
    uid = await _get_current_user_id(request, access_token)
    if not uid:
        raise HTTPException(status_code=401, detail="Не авторизован")

    body = await request.json()
    text = (body.get("text") or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Введите сообщение")

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        # Verify ownership
        ticket = await ticket_svc.get_ticket(uow, ticket_id)
        if not ticket or ticket.user_telegram_id != uid:
            raise HTTPException(status_code=404, detail="Тикет не найден")
        if ticket.status == "CLOSED":
            raise HTTPException(status_code=400, detail="Тикет закрыт")

        updated = await ticket_svc.add_reply(uow, ticket_id, uid, text, is_admin=False)
        return JSONResponse(_ticket_to_dict(updated))


@router.post("/api/tickets/{ticket_id}/close")
async def api_close_ticket(ticket_id: int, request: Request, access_token: Optional[str] = Cookie(default=None)):
    """User: close own ticket."""
    uid = await _get_current_user_id(request, access_token)
    if not uid:
        raise HTTPException(status_code=401, detail="Не авторизован")

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        ticket = await ticket_svc.get_ticket(uow, ticket_id)
        if not ticket or ticket.user_telegram_id != uid:
            raise HTTPException(status_code=404, detail="Тикет не найден")
        closed = await ticket_svc.close_ticket(uow, ticket_id)
        return JSONResponse(_ticket_to_dict(closed))


# ── Admin Tickets ─────────────────────────────────────────────


@router.get("/api/admin/tickets")
async def api_admin_get_tickets(request: Request, access_token: Optional[str] = Cookie(default=None)):
    await _require_admin(request, access_token)

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        tickets = await ticket_svc.get_all_tickets(uow)
        return JSONResponse([_ticket_to_dict(t) for t in tickets])


@router.get("/api/admin/tickets/{ticket_id}")
async def api_admin_get_ticket(ticket_id: int, request: Request, access_token: Optional[str] = Cookie(default=None)):
    await _require_admin(request, access_token)

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        ticket = await ticket_svc.get_ticket(uow, ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Тикет не найден")
        await ticket_svc.mark_read_by_admin(uow, ticket_id)
        return JSONResponse(_ticket_to_dict(ticket))


@router.post("/api/admin/tickets/{ticket_id}/reply")
async def api_admin_reply_ticket(ticket_id: int, request: Request, access_token: Optional[str] = Cookie(default=None)):
    uid = await _require_admin(request, access_token)

    body = await request.json()
    text = (body.get("text") or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Введите сообщение")

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        updated = await ticket_svc.add_reply(uow, ticket_id, uid, text, is_admin=True)
        if not updated:
            raise HTTPException(status_code=404, detail="Тикет не найден")

        return JSONResponse(_ticket_to_dict(updated))


@router.post("/api/admin/tickets/{ticket_id}/close")
async def api_admin_close_ticket(ticket_id: int, request: Request, access_token: Optional[str] = Cookie(default=None)):
    await _require_admin(request, access_token)

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        closed = await ticket_svc.close_ticket(uow, ticket_id)
        if not closed:
            raise HTTPException(status_code=404, detail="Тикет не найден")
        return JSONResponse(_ticket_to_dict(closed))


@router.delete("/api/admin/tickets/{ticket_id}")
async def api_admin_delete_ticket(ticket_id: int, request: Request, access_token: Optional[str] = Cookie(default=None)):
    await _require_admin(request, access_token)

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        deleted = await ticket_svc.delete_ticket(uow, ticket_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Тикет не найден")
        return JSONResponse({"ok": True})
