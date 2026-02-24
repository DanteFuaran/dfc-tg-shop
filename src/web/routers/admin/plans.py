"""Admin plan management routes."""

from __future__ import annotations

from decimal import Decimal

from dishka import AsyncContainer, Scope
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from src.core.enums import Currency, PlanAvailability, PlanType
from src.infrastructure.database.models.dto.plan import PlanDto, PlanDurationDto, PlanPriceDto
from src.services.plan import PlanService
from src.web.dependencies import require_admin

router = APIRouter(prefix="/api/admin/plans", tags=["admin-plans"])


@router.get("")
async def api_admin_plans(request: Request, uid: int = Depends(require_admin)):
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


@router.post("")
async def api_admin_create_plan(request: Request, uid: int = Depends(require_admin)):
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
        durations = _parse_durations(body.get("durations", []))

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


@router.put("/{plan_id}")
async def api_admin_update_plan(plan_id: int, request: Request, uid: int = Depends(require_admin)):
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
            existing.durations = _parse_durations(body["durations"])

        updated = await plan_service.update(existing)
        if not updated:
            raise HTTPException(status_code=500, detail="Ошибка обновления тарифа")
        return JSONResponse({"ok": True})


@router.delete("/{plan_id}")
async def api_admin_delete_plan(plan_id: int, request: Request, uid: int = Depends(require_admin)):
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        plan_service: PlanService = await req_container.get(PlanService)
        result = await plan_service.delete(plan_id)
        if not result:
            raise HTTPException(status_code=404, detail="Тариф не найден")
        return JSONResponse({"ok": True})


@router.patch("/{plan_id}/toggle")
async def api_admin_toggle_plan(plan_id: int, request: Request, uid: int = Depends(require_admin)):
    """Toggle is_active for a plan."""
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


# ── Helper ────────────────────────────────────────────────────────


def _parse_durations(raw: list[dict]) -> list[PlanDurationDto]:
    """Parse durations list from request body (DRY — used in create & update)."""
    durations: list[PlanDurationDto] = []
    for dur_data in raw:
        prices: list[PlanPriceDto] = []
        for price_data in dur_data.get("prices", []):
            try:
                currency = Currency(price_data.get("currency", "RUB"))
            except (ValueError, KeyError):
                currency = Currency.RUB
            prices.append(PlanPriceDto(
                currency=currency,
                price=Decimal(str(price_data.get("amount", "0"))),
            ))
        durations.append(PlanDurationDto(
            days=int(dur_data.get("days", 30)),
            prices=prices,
        ))
    return durations
