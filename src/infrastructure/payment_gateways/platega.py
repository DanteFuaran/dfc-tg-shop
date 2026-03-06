import hashlib
import hmac
import json
import uuid
from decimal import Decimal
from typing import Any, Final
from uuid import UUID

import orjson
from aiogram import Bot
from fastapi import Request
from httpx import AsyncClient, HTTPStatusError
from loguru import logger

from src.core.config import AppConfig
from src.core.enums import TransactionStatus
from src.infrastructure.database.models.dto import (
    PaymentGatewayDto,
    PaymentResult,
    PlategaGatewaySettingsDto,
)

from .base import BasePaymentGateway


class PlategaGateway(BasePaymentGateway):
    _client: AsyncClient

    API_BASE: Final[str] = "https://platega.com"

    def __init__(self, gateway: PaymentGatewayDto, bot: Bot, config: AppConfig) -> None:
        super().__init__(gateway, bot, config)

        if not isinstance(self.data.settings, PlategaGatewaySettingsDto):
            raise TypeError(
                f"Invalid settings type: expected {PlategaGatewaySettingsDto.__name__}, "
                f"got {type(self.data.settings).__name__}"
            )

        self._client = self._make_client(base_url=self.API_BASE)

    async def handle_create_payment(self, amount: Decimal, details: str) -> PaymentResult:
        order_id = str(uuid.uuid4())
        payload = await self._create_payment_payload(str(amount), order_id, details)
        signature = self._generate_signature(payload)

        try:
            response = await self._client.post(
                "/api/v2/create",
                json={**payload, "sign": signature},
            )
            response.raise_for_status()
            data = orjson.loads(response.content)
            return self._get_payment_data(data, order_id)

        except HTTPStatusError as exception:
            logger.error(
                f"HTTP error creating Platega payment. "
                f"Status: '{exception.response.status_code}', Body: {exception.response.text}"
            )
            raise
        except (KeyError, orjson.JSONDecodeError) as exception:
            logger.error(f"Failed to parse Platega response. Error: {exception}")
            raise
        except Exception as exception:
            logger.exception(f"An unexpected error occurred while creating Platega payment: {exception}")
            raise

    async def handle_webhook(self, request: Request) -> tuple[UUID, TransactionStatus]:
        logger.debug("Received Platega webhook request")
        webhook_data = await self._get_webhook_data(request)

        if not self._verify_webhook(webhook_data):
            raise PermissionError("Platega webhook verification failed")

        order_id = webhook_data.get("order_id")
        if not order_id:
            raise ValueError("Required field 'order_id' is missing")

        status = webhook_data.get("status")
        payment_id = UUID(order_id)

        match status:
            case "success" | "paid":
                transaction_status = TransactionStatus.COMPLETED
            case "cancel" | "expired" | "failed":
                transaction_status = TransactionStatus.CANCELED
            case _:
                raise ValueError(f"Unsupported Platega status: {status}")

        return payment_id, transaction_status

    async def _create_payment_payload(self, amount: str, order_id: str, details: str) -> dict[str, Any]:
        return {
            "amount": float(amount),
            "order_id": order_id,
            "shop_id": self.data.settings.shop_id,  # type: ignore[union-attr]
            "webhook_url": self.config.get_webhook(self.data.type),
            "success_url": await self._get_bot_redirect_url(),
            "fail_url": await self._get_bot_redirect_url(),
            "description": details,
        }

    def _generate_signature(self, payload: dict) -> str:
        """Generate signature for Platega API."""
        sorted_values = ":".join(str(payload[k]) for k in sorted(payload.keys()))
        secret = self.data.settings.secret_key.get_secret_value()  # type: ignore[union-attr]
        sign_str = f"{sorted_values}:{secret}"
        return hashlib.sha256(sign_str.encode("utf-8")).hexdigest()

    def _get_payment_data(self, data: dict[str, Any], order_id: str) -> PaymentResult:
        payment_url = data.get("url") or data.get("payment_url")

        if not payment_url:
            raise KeyError("Invalid response from Platega API: missing 'url'")

        return PaymentResult(id=UUID(order_id), url=str(payment_url))

    def _verify_webhook(self, data: dict) -> bool:
        """Verify Platega webhook signature."""
        sign = data.pop("sign", None)
        if not sign:
            raise ValueError("Missing signature in Platega webhook")

        sorted_values = ":".join(str(data[k]) for k in sorted(data.keys()))
        secret = self.data.settings.secret_key.get_secret_value()  # type: ignore[union-attr]
        sign_str = f"{sorted_values}:{secret}"
        computed = hashlib.sha256(sign_str.encode("utf-8")).hexdigest()

        if not hmac.compare_digest(computed, sign):
            logger.warning("Invalid Platega webhook signature")
            return False

        return True
