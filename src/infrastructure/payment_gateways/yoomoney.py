import hashlib
import uuid
from decimal import Decimal
from typing import Any, Final, Literal
from urllib.parse import parse_qs
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
    YoomoneyGatewaySettingsDto,
)

from .base import BasePaymentGateway


# Специальный тип для обозначения тестового webhook'а
TEST_WEBHOOK = "TEST_WEBHOOK"


class YoomoneyGateway(BasePaymentGateway):
    _client: AsyncClient

    API_BASE: Final[str] = "https://yoomoney.ru"
    PAY_FORM: Final[str] = "button"
    PAY_TYPE: Final[str] = "AC"

    def __init__(self, gateway: PaymentGatewayDto, bot: Bot, config: AppConfig) -> None:
        super().__init__(gateway, bot, config)

        if not isinstance(self.data.settings, YoomoneyGatewaySettingsDto):
            raise TypeError(
                f"Invalid settings type: expected {YoomoneyGatewaySettingsDto.__name__}, "
                f"got {type(self.data.settings).__name__}"
            )

        self._client = self._make_client(base_url=self.API_BASE)

    async def handle_create_payment(self, amount: Decimal, details: str) -> PaymentResult:
        payment_id = uuid.uuid4()
        payload = await self._create_payment_payload(str(amount), str(payment_id))

        try:
            response = await self._client.post(
                "quickpay/confirm.xml",
                data=payload,
                follow_redirects=True,
            )
            response.raise_for_status()
            return PaymentResult(id=payment_id, url=str(response.url))

        except HTTPStatusError as exception:
            logger.error(
                f"HTTP error creating payment. "
                f"Status: '{exception.response.status_code}', Body: {exception.response.text}"
            )
            raise
        except (KeyError, orjson.JSONDecodeError) as exception:
            logger.error(f"Failed to parse response. Error: {exception}")
            raise
        except Exception as exception:
            logger.exception(f"An unexpected error occurred while creating payment: {exception}")
            raise

    async def handle_webhook(self, request: Request) -> tuple[UUID, TransactionStatus] | Literal["TEST_WEBHOOK"]:
        logger.debug("Received YooMoney webhook request")
        webhook_data = await self._get_webhook_data(request)
        operation_id = webhook_data.get("operation_id")

        if operation_id == "test-notification":
            logger.info("Received test notification from YooMoney")
            return TEST_WEBHOOK

        if not self._verify_webhook(webhook_data):
            raise ValueError("YooMoney verification failed")

        payment_id_str = webhook_data.get("label")

        if not payment_id_str:
            raise ValueError("Required field 'label' is missing")

        payment_id = UUID(payment_id_str)
        transaction_status = TransactionStatus.COMPLETED

        # Возвращаем сумму из webhook для последующей верификации
        webhook_amount = webhook_data.get("withdraw_amount") or webhook_data.get("amount")

        return payment_id, transaction_status

    async def _get_webhook_data(self, request: Request) -> dict:
        try:
            body_bytes = await request.body()
            body_str = body_bytes.decode("utf-8")
            parsed = parse_qs(body_str)
            data = {k: v[0] for k, v in parsed.items()}
            logger.info(f"YooMoney webhook fields: { {k: v for k, v in data.items() if k != 'sha1_hash'} }")
            return data
        except Exception as exception:
            logger.error(f"Failed to parse webhook payload: {exception}")
            raise ValueError("Invalid webhook payload") from exception

    async def _create_payment_payload(
        self,
        amount: str,
        label: str,
    ) -> dict[str, Any]:
        return {
            "receiver": self.data.settings.wallet_id,  # type: ignore[union-attr]
            "quickpay-form": self.PAY_FORM,
            "paymentType": self.PAY_TYPE,
            "sum": amount,
            "label": label,
            "successURL": await self._get_bot_redirect_url(),
        }

    def _verify_webhook(self, data: dict) -> bool:
        notification_type = data.get("notification_type", "")
        operation_id = data.get("operation_id", "")
        amount = data.get("amount", "")
        currency = data.get("currency", "")
        dt = data.get("datetime", "")
        sender = data.get("sender", "")
        codepro = data.get("codepro", "")
        secret = self.data.settings.secret_key.get_secret_value()  # type: ignore[union-attr]
        label = data.get("label", "")

        params = [
            notification_type,
            operation_id,
            amount,
            currency,
            dt,
            sender,
            codepro,
            secret,
            label,
        ]

        sign_str = "&".join(params)
        computed_hash = hashlib.sha1(sign_str.encode("utf-8")).hexdigest()

        is_valid: bool = computed_hash == data.get("sha1_hash", "")
        if not is_valid:
            logger.warning(
                f"Invalid signature. Expected {computed_hash}, received {data.get('sha1_hash')}\n"
                f"  Fields used in hash:\n"
                f"    notification_type = {notification_type!r}\n"
                f"    operation_id      = {operation_id!r}\n"
                f"    amount            = {amount!r}\n"
                f"    currency          = {currency!r}\n"
                f"    datetime          = {dt!r}\n"
                f"    sender            = {(sender[:3] + '***') if sender else ''!r}\n"
                f"    codepro           = {codepro!r}\n"
                f"    secret            = {'*' * len(secret)!r} (len={len(secret)})\n"
                f"    label             = {label!r}\n"
                f"  Sign string (redacted): {sign_str.replace(secret, '*' * len(secret))!r}"
            )

        return is_valid
