"""Purchase, trial, top-up, and promocode routes."""

from __future__ import annotations

from decimal import Decimal

from dishka import AsyncContainer, Scope
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from loguru import logger

from src.core.enums import (
    Currency,
    PaymentGatewayType,
    PurchaseType,
    ReferralRewardType,
)
from src.infrastructure.database.models.dto.plan import PlanSnapshotDto
from src.services.payment_gateway import PaymentGatewayService
from src.services.plan import PlanService
from src.services.pricing import PricingService
from src.services.promocode import PromocodeService
from src.services.referral import ReferralService
from src.services.remnawave import RemnawaveService
from src.services.settings import SettingsService
from src.services.subscription import SubscriptionService
from src.services.user import UserService
from src.web.dependencies import require_auth

router = APIRouter(prefix="/api", tags=["purchase"])


@router.post("/purchase")
async def api_purchase(request: Request, uid: int = Depends(require_auth)):
    """User: purchase a plan with balance."""
    body = await request.json()
    plan_id = body.get("plan_id")
    duration_days = body.get("duration_days")
    gateway = body.get("gateway")
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

        base_price = Decimal(str(price_obj))

        global_discount = settings.features.global_discount if hasattr(settings.features, 'global_discount') else None
        price = pricing_service.calculate(user, base_price, currency, global_discount, context="subscription")

        # Check balance (with combined mode support)
        is_combined = await settings_service.is_balance_combined()
        referral_balance = await referral_service.get_pending_rewards_amount(
            telegram_id=uid, reward_type=ReferralRewardType.MONEY,
        )
        available = user.balance + referral_balance if is_combined else user.balance

        # Determine purchase type
        current_sub = await subscription_service.get_current(telegram_id=uid)
        if current_sub and current_sub.status in ["ACTIVE", "active"]:
            # Trial/referral → treat as NEW (full plan update in Remnawave)
            if current_sub.is_trial or (current_sub.plan and current_sub.plan.name and any(
                kw in current_sub.plan.name.lower() for kw in ("пробн", "trial", "реферал", "referral")
            )):
                purchase_type = PurchaseType.NEW
            else:
                # Check if user is changing to a different plan (replace duration) vs renewing same plan (extend)
                current_plan_id = current_sub.plan_id if hasattr(current_sub, 'plan_id') else (current_sub.plan.id if current_sub.plan else None)
                if current_plan_id and current_plan_id != plan_id:
                    purchase_type = PurchaseType.CHANGE
                else:
                    purchase_type = PurchaseType.RENEW
        else:
            purchase_type = PurchaseType.NEW

        plan_snapshot = PlanSnapshotDto.from_plan(plan, duration_days)

        # Gateway payment (non-balance)
        if gateway and gateway != "balance":
            try:
                gw_type = PaymentGatewayType(gateway)
                result = await payment_gw.create_payment(
                    user=user, plan=plan_snapshot, pricing=price,
                    purchase_type=purchase_type, gateway_type=gw_type,
                )
                payment_url = result.url if hasattr(result, 'url') else None
                if payment_url:
                    return JSONResponse({"ok": True, "payment_url": payment_url})
                return JSONResponse({"ok": True})
            except Exception as e:
                logger.exception(f"Gateway purchase failed for user {uid}: {e}")
                raise HTTPException(status_code=500, detail="Ошибка обработки покупки через платёжную систему")

        # Balance payment
        if available < price.final_amount:
            raise HTTPException(status_code=400, detail="Недостаточно средств")

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


@router.post("/trial/activate")
async def api_trial_activate(request: Request, uid: int = Depends(require_auth)):
    """User: activate trial subscription."""
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


@router.post("/topup")
async def api_topup(request: Request, uid: int = Depends(require_auth)):
    """User: top up balance via payment gateway."""
    body = await request.json()
    amount = body.get("amount")
    gateway_type = body.get("gateway")
    if not amount or not gateway_type:
        raise HTTPException(status_code=400, detail="Укажите amount и gateway")

    amount = int(amount)
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Сумма должна быть больше 0")

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        user_service: UserService = await req_container.get(UserService)
        payment_gw: PaymentGatewayService = await req_container.get(PaymentGatewayService)
        settings_service: SettingsService = await req_container.get(SettingsService)

        user = await user_service.get(telegram_id=uid)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        settings = await settings_service.get()
        min_amt = settings.balance_min_amount if hasattr(settings, 'balance_min_amount') else 10
        max_amt = settings.balance_max_amount if hasattr(settings, 'balance_max_amount') else 100000
        if amount < min_amt:
            raise HTTPException(status_code=400, detail=f"Минимальная сумма: {min_amt}")
        if amount > max_amt:
            raise HTTPException(status_code=400, detail=f"Максимальная сумма: {max_amt}")

        try:
            gw_type = PaymentGatewayType(gateway_type)
            result = await payment_gw.create_topup_payment(
                user=user, amount=amount, gateway_type=gw_type,
            )
            payment_url = result.payment_url if hasattr(result, 'payment_url') else None
            if payment_url:
                return JSONResponse({"ok": True, "payment_url": payment_url})
            return JSONResponse({"ok": True})
        except Exception as e:
            logger.exception(f"Topup failed for user {uid}: {e}")
            raise HTTPException(status_code=500, detail="Ошибка создания платежа")


@router.post("/promocode/activate")
async def api_activate_promocode(request: Request, uid: int = Depends(require_auth)):
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
