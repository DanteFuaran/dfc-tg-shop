"""Admin broadcast management routes."""

from __future__ import annotations

import uuid
from typing import Optional

from dishka import AsyncContainer, Scope
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from src.core.enums import BroadcastAudience, BroadcastStatus
from src.core.utils.message_payload import MessagePayload
from src.infrastructure.database.models.dto import BroadcastDto
from src.infrastructure.taskiq.tasks.broadcast import send_broadcast_task
from src.services.broadcast import BroadcastService
from src.web.dependencies import require_admin

router = APIRouter(prefix="/api/admin/broadcast", tags=["admin-broadcast"])

_AUDIENCE_LABELS = {
    "ALL": "Все пользователи",
    "SUBSCRIBED": "С активной подпиской",
    "UNSUBSCRIBED": "Без подписки",
    "EXPIRED": "С истёкшей подпиской",
    "TRIAL": "С триальной подпиской",
    "PLAN": "По тарифу",
}


def _serialize_broadcast(b: BroadcastDto) -> dict:
    return {
        "id": b.id,
        "task_id": str(b.task_id),
        "status": b.status.value if hasattr(b.status, "value") else str(b.status),
        "audience": b.audience.value if hasattr(b.audience, "value") else str(b.audience),
        "total_count": b.total_count,
        "success_count": b.success_count,
        "failed_count": b.failed_count,
        "created_at": b.created_at.strftime("%d.%m.%Y %H:%M") if b.created_at else "—",
        "text": b.payload.text or "" if b.payload else "",
    }


@router.get("")
async def api_admin_broadcast_list(
    request: Request,
    uid: int = Depends(require_admin),
):
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        broadcast_service: BroadcastService = await req_container.get(BroadcastService)
        broadcasts = await broadcast_service.get_all()
        return JSONResponse([_serialize_broadcast(b) for b in broadcasts])


@router.post("")
async def api_admin_broadcast_create(
    request: Request,
    uid: int = Depends(require_admin),
):
    body = await request.json()
    text: Optional[str] = body.get("text", "").strip()
    audience_str: str = body.get("audience", "ALL")
    plan_id: Optional[int] = body.get("plan_id")

    if not text:
        raise HTTPException(status_code=400, detail="Текст сообщения обязателен")

    try:
        audience = BroadcastAudience(audience_str.upper())
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Неверная аудитория: {audience_str}")

    task_id = uuid.uuid4()
    payload = MessagePayload(text=text, auto_delete_after=None, add_close_button=True)

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        broadcast_service: BroadcastService = await req_container.get(BroadcastService)

        broadcast_dto = BroadcastDto(
            task_id=task_id,
            status=BroadcastStatus.PROCESSING,
            audience=audience,
            payload=payload,
        )
        created = await broadcast_service.create(broadcast_dto)

        users = await broadcast_service.get_audience_users(
            audience=audience,
            plan_id=plan_id if audience == BroadcastAudience.PLAN else None,
        )

        try:
            await (
                send_broadcast_task.kicker()
                .with_task_id(str(task_id))
                .kiq(created, users, payload)
            )
        except Exception as e:
            # Mark as error if dispatch fails
            created.status = BroadcastStatus.ERROR
            await broadcast_service.update(created)
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка постановки задачи: {e}",
            )

        return JSONResponse(_serialize_broadcast(created), status_code=201)


@router.delete("/{broadcast_id}")
async def api_admin_broadcast_delete(
    broadcast_id: int,
    request: Request,
    uid: int = Depends(require_admin),
):
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        broadcast_service: BroadcastService = await req_container.get(BroadcastService)
        await broadcast_service.delete_broadcast(broadcast_id)
        return JSONResponse({"ok": True})
