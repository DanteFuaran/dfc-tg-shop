"""Admin promocode management routes."""

from __future__ import annotations

from typing import Optional

from dishka import AsyncContainer, Scope
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from src.core.enums import PromocodeAvailability, PromocodeRewardType
from src.infrastructure.database.models.dto import PromocodeDto
from src.services.promocode import PromocodeService
from src.web.dependencies import require_admin

router = APIRouter(prefix="/api/admin/promocodes", tags=["admin-promocodes"])


def _serialize_promo(p: PromocodeDto) -> dict:
    activations_count = len(p.activations) if p.activations else 0
    return {
        "id": p.id,
        "code": p.code,
        "name": p.name,
        "is_active": p.is_active,
        "reward_type": p.reward_type.value if hasattr(p.reward_type, "value") else str(p.reward_type),
        "reward": p.reward,
        "availability": p.availability.value if hasattr(p.availability, "value") else str(p.availability),
        "lifetime": p.lifetime,
        "max_activations": p.max_activations,
        "activations_count": activations_count,
        "is_expired": p.is_expired,
        "is_depleted": p.is_depleted,
        "created_at": p.created_at.strftime("%d.%m.%Y") if p.created_at else "—",
    }


@router.get("")
async def api_admin_promo_list(
    request: Request,
    uid: int = Depends(require_admin),
):
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        promo_service: PromocodeService = await req_container.get(PromocodeService)
        promos = await promo_service.get_all()
        return JSONResponse([_serialize_promo(p) for p in promos])


@router.post("")
async def api_admin_promo_create(
    request: Request,
    uid: int = Depends(require_admin),
):
    body = await request.json()

    code: str = body.get("code", "").strip()
    name: str = body.get("name", "").strip()
    reward_type_str: str = body.get("reward_type", "DURATION")
    reward: Optional[int] = body.get("reward", 1)
    availability_str: str = body.get("availability", "ALL")
    lifetime: Optional[int] = body.get("lifetime")
    max_activations: Optional[int] = body.get("max_activations")

    try:
        reward_type = PromocodeRewardType(reward_type_str.upper())
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Неверный тип награды: {reward_type_str}")

    try:
        availability = PromocodeAvailability(availability_str.upper())
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Неверная доступность: {availability_str}")

    # Auto-generate code if empty
    if not code:
        code = PromocodeDto.generate_code()

    dto = PromocodeDto(
        code=code,
        name=name,
        is_active=True,
        reward_type=reward_type,
        reward=reward,
        availability=availability,
        lifetime=lifetime if lifetime and lifetime > 0 else None,
        max_activations=max_activations if max_activations and max_activations > 0 else None,
    )

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        promo_service: PromocodeService = await req_container.get(PromocodeService)

        # Check code uniqueness
        existing = await promo_service.get_by_code(code)
        if existing:
            raise HTTPException(status_code=409, detail="Промокод с таким кодом уже существует")

        created = await promo_service.create(dto)
        if not created:
            raise HTTPException(status_code=500, detail="Не удалось создать промокод")

        return JSONResponse(_serialize_promo(created), status_code=201)


@router.patch("/{promo_id}/toggle")
async def api_admin_promo_toggle(
    promo_id: int,
    request: Request,
    uid: int = Depends(require_admin),
):
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        promo_service: PromocodeService = await req_container.get(PromocodeService)
        promo = await promo_service.get(promo_id)
        if not promo:
            raise HTTPException(status_code=404, detail="Промокод не найден")
        promo.is_active = not promo.is_active
        updated = await promo_service.update(promo)
        return JSONResponse(_serialize_promo(updated or promo))


@router.delete("/{promo_id}")
async def api_admin_promo_delete(
    promo_id: int,
    request: Request,
    uid: int = Depends(require_admin),
):
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        promo_service: PromocodeService = await req_container.get(PromocodeService)
        promo = await promo_service.get(promo_id)
        if not promo:
            raise HTTPException(status_code=404, detail="Промокод не найден")
        ok = await promo_service.delete(promo_id)
        return JSONResponse({"ok": bool(ok)})
