import traceback

from aiogram.utils.formatting import Text
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Request, Response, status
from loguru import logger

from src.core.constants import API_V1, PAYMENTS_WEBHOOK_PATH
from src.core.enums import PaymentGatewayType, SystemNotificationType
from src.core.utils.message_payload import MessagePayload
from src.infrastructure.taskiq.tasks.payments import handle_payment_transaction_task
from src.services.notification import NotificationService
from src.services.payment_gateway import PaymentGatewayService

router = APIRouter(prefix=API_V1 + PAYMENTS_WEBHOOK_PATH)


@router.post("/{gateway_type}")
@inject
async def payments_webhook(
    gateway_type: str,
    request: Request,
    payment_gateway_service: FromDishka[PaymentGatewayService],
    notification_service: FromDishka[NotificationService],
) -> Response:
    try:
        gateway_enum = PaymentGatewayType(gateway_type.upper())
    except ValueError:
        logger.exception(f"Invalid gateway type received: '{gateway_type}'")
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    try:
        # Сначала проверяем, активен ли шлюз, до создания инстанса
        gateway_data = await payment_gateway_service.get_by_type(gateway_enum)
        if not gateway_data:
            logger.warning(f"Webhook received for unknown payment gateway {gateway_enum}")
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        
        if not gateway_data.is_active:
            logger.warning(f"Webhook received for disabled payment gateway {gateway_enum}")
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        
        gateway = await payment_gateway_service._get_gateway_instance(gateway_enum)
        result = await gateway.handle_webhook(request)
        
        # Если это тестовый webhook, отправляем уведомление администратору
        if result == "TEST_WEBHOOK":
            logger.info(f"Test webhook from {gateway_enum} received successfully")
            await notification_service.system_notify(
                payload=MessagePayload.not_deleted(
                    i18n_key="ntf-event-test-webhook-success",
                    i18n_kwargs={
                        "gateway_name": gateway_data.type.value,
                        "gateway_type": gateway_enum.value,
                    },
                    close_button_style="success",
                ),
                ntf_type=SystemNotificationType.BILLING,
            )
            return Response(status_code=status.HTTP_200_OK)
        
        payment_id, payment_status = result
        await handle_payment_transaction_task.kiq(payment_id, payment_status)
        return Response(status_code=status.HTTP_200_OK)

    except Exception as exception:
        logger.exception(f"Error processing webhook for '{gateway_type}': {exception}")
        traceback_str = traceback.format_exc()
        error_type_name = type(exception).__name__
        error_message_str = str(exception)[:512]
        
        # Отправляем уведомление об ошибке (может быть тестовый webhook с ошибкой)
        await notification_service.system_notify(
            payload=MessagePayload.not_deleted(
                i18n_key="ntf-event-test-webhook-failed",
                i18n_kwargs={
                    "gateway_type": gateway_type.upper(),
                    "error_type": error_type_name,
                    "error_message": error_message_str,
                },
            ),
            ntf_type=SystemNotificationType.BILLING,
        )

        await notification_service.error_notify(
            traceback_str=traceback_str,
            payload=MessagePayload.not_deleted(
                i18n_key="ntf-event-error",
                i18n_kwargs={
                    "user": False,
                    "error": f"{error_type_name}: {error_message.as_html()}",
                },
            ),
        )
    finally:
        return Response(status_code=status.HTTP_200_OK)
