"""Admin user management routes."""

from __future__ import annotations

from dishka import AsyncContainer, Scope
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from src.core.enums import ReferralRewardType, UserRole
from src.services.referral import ReferralService
from src.services.subscription import SubscriptionService
from src.services.user import UserService
from src.web.dependencies import require_admin

router = APIRouter(prefix="/api/admin/users", tags=["admin-users"])


@router.get("")
async def api_admin_users(request: Request, uid: int = Depends(require_admin)):
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


@router.get("/{tid}")
async def api_admin_user_detail(tid: int, request: Request, uid: int = Depends(require_admin)):
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


@router.post("/{tid}/role")
async def api_admin_set_role(tid: int, request: Request, uid: int = Depends(require_admin)):
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


@router.post("/{tid}/balance")
async def api_admin_set_balance(tid: int, request: Request, uid: int = Depends(require_admin)):
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


@router.post("/{tid}/bonus-balance")
async def api_admin_set_bonus_balance(tid: int, request: Request, uid: int = Depends(require_admin)):
    """Admin: modify user bonus balance via referral rewards."""
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


@router.post("/{tid}/block")
async def api_admin_toggle_block(tid: int, request: Request, uid: int = Depends(require_admin)):
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
