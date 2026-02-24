"""Admin payment gateway routes."""

from __future__ import annotations

from typing import Any, Optional

from dishka import AsyncContainer, Scope
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import SecretStr

from src.services.payment_gateway import PaymentGatewayService
from src.web.dependencies import require_admin

router = APIRouter(prefix="/api/admin/gateways", tags=["admin-gateways"])


@router.get("")
async def api_admin_gateways(request: Request, uid: int = Depends(require_admin)):
    """Return all payment gateways (for admin settings)."""
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


@router.patch("/{gateway_id}")
async def api_admin_update_gateway(
    gateway_id: int, request: Request, uid: int = Depends(require_admin),
):
    """Update a payment gateway (toggle is_active, update settings fields)."""
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
