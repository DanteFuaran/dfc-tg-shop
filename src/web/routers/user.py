"""User data, config, credentials, subscription routes."""

from __future__ import annotations

from typing import Any, Optional

from aiogram import Bot
from dishka import AsyncContainer, Scope
from fastapi import APIRouter, Cookie, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from loguru import logger

from src.core.config import AppConfig
from src.core.enums import ReferralRewardType
from src.infrastructure.database import UnitOfWork
from src.infrastructure.database.models.dto.plan import PlanSnapshotDto
from src.infrastructure.database.models.sql.web_credential import WebCredential
from src.services.payment_gateway import PaymentGatewayService
from src.services.plan import PlanService
from src.services.referral import ReferralService
from src.services.remnawave import RemnawaveService
from src.services.settings import SettingsService
from src.services.subscription import SubscriptionService
from src.services.ticket import TicketService
from src.services.user import UserService
from src.web.auth import hash_password, verify_password
from src.web.dependencies import require_auth

router = APIRouter(prefix="/api", tags=["user"])


# ── Helpers ───────────────────────────────────────────────────────


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
                "referral_invite_message": settings.referral.invite_message or "" if hasattr(settings, "referral") else "",
                "promocodes_enabled": features.promocodes_enabled,
            }
        except Exception:
            pass

        # Referral balance + ref link for profile display
        referral_balance_user = 0
        ref_link = ""
        try:
            ref_svc: ReferralService = await req_container.get(ReferralService)
            referral_balance_user = await ref_svc.get_pending_rewards_amount(telegram_id=telegram_id, reward_type=ReferralRewardType.MONEY)
            user_ref_code = user.referral_code if hasattr(user, 'referral_code') and user.referral_code else str(telegram_id)
            ref_link = await ref_svc.get_ref_link(user_ref_code)
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
            has_any_sub = bool(sub_data)  # user has current subscription
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

        # Available payment gateways (active, excluding BALANCE type)
        available_gateways = []
        try:
            payment_gw: PaymentGatewayService = await req_container.get(PaymentGatewayService)
            gw_active = await payment_gw.filter_active()
            for gw in gw_active:
                gw_type = gw.type.value if hasattr(gw.type, "value") else str(gw.type)
                if gw_type == "BALANCE":
                    continue
                available_gateways.append({
                    "type": gw_type,
                    "currency": gw.currency.value if hasattr(gw.currency, "value") else str(gw.currency),
                })
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
            "ref_link": ref_link,
            "features": features_data,
            "support_url": support_url,
            "trial_available": trial_available,
            "default_currency": default_currency,
            "bot_locale": bot_locale,
            "ticket_unread": ticket_unread,
            "has_open_tickets": has_open_tickets,
            "available_gateways": available_gateways,
        }


# ══════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════


@router.get("/config")
async def api_config(request: Request, uid: int = Depends(require_auth)):
    config: AppConfig = request.app.state.config
    domain = config.domain.get_secret_value() if config.domain else ""
    support_username = ""
    try:
        support_username = config.bot.support_username.get_secret_value() if config.bot.support_username else ""
    except Exception:
        pass
    return JSONResponse({"domain": domain, "support_username": support_username})


# ══════════════════════════════════════════════════════════════════
# TICKETS STATUS (lightweight polling endpoint)
# ══════════════════════════════════════════════════════════════════


@router.get("/tickets/status")
async def api_tickets_status(request: Request, uid: int = Depends(require_auth)):
    """Lightweight endpoint for polling ticket status (FAB badge)."""
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
        result: dict[str, Any] = {"has_open": has_open, "unread": unread}
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


# ══════════════════════════════════════════════════════════════════
# USER DATA & CREDENTIALS
# ══════════════════════════════════════════════════════════════════


@router.post("/user/credentials")
async def api_user_set_credentials(request: Request, uid: int = Depends(require_auth)):
    """Set or update web login credentials for the current user."""
    body = await request.json()
    web_username = body.get("web_username", "").strip()
    password = body.get("password", "")
    if len(web_username) < 3:
        raise HTTPException(status_code=400, detail="Логин должен быть не менее 3 символов")
    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Пароль должен быть не менее 6 символов")

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        existing = await uow.repository.web_credentials.get_by_telegram_id(uid)
        username_taken = await uow.repository.web_credentials.get_by_username(web_username)
        if username_taken and (not existing or username_taken.telegram_id != uid):
            raise HTTPException(status_code=409, detail="Этот логин уже занят")
        password_hash = hash_password(password)
        if existing:
            await uow.repository.web_credentials.delete(uid)
        credential = WebCredential(telegram_id=uid, web_username=web_username, password_hash=password_hash)
        await uow.repository.web_credentials.create(credential)
        try:
            await uow.commit()
        except Exception:
            raise HTTPException(status_code=500, detail="Ошибка при сохранении")
    return JSONResponse({"ok": True})


@router.post("/user/credentials/password")
async def api_user_change_password(request: Request, uid: int = Depends(require_auth)):
    """Change web login password (requires old password verification)."""
    body = await request.json()
    old_password = body.get("old_password", "")
    new_password = body.get("new_password", "")
    if len(new_password) < 6:
        raise HTTPException(status_code=400, detail="Новый пароль должен быть не менее 6 символов")

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        cred = await uow.repository.web_credentials.get_by_telegram_id(uid)
        if not cred:
            raise HTTPException(status_code=404, detail="Учётные данные не найдены")
        if not verify_password(old_password, cred.password_hash):
            raise HTTPException(status_code=403, detail="Неверный текущий пароль")
        new_hash = hash_password(new_password)
        await uow.repository.web_credentials.update_password(uid, new_hash)
        try:
            await uow.commit()
        except Exception:
            raise HTTPException(status_code=500, detail="Ошибка при сохранении")
    return JSONResponse({"ok": True})


@router.get("/user/data")
async def api_user_data(request: Request, uid: int = Depends(require_auth)):
    data = await _build_user_data(request, uid)
    if not data:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return JSONResponse(data)


@router.get("/user/subscription")
async def api_user_subscription(request: Request, uid: int = Depends(require_auth)):
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
