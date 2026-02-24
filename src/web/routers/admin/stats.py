"""Admin statistics routes."""

from __future__ import annotations

from dishka import AsyncContainer, Scope
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from src.services.subscription import SubscriptionService
from src.services.user import UserService
from src.web.dependencies import require_admin

router = APIRouter(prefix="/api/admin", tags=["admin-stats"])


@router.get("/stats")
async def api_admin_stats(request: Request, uid: int = Depends(require_admin)):
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
