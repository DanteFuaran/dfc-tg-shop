from datetime import timedelta
from uuid import UUID

from dishka.integrations.taskiq import FromDishka, inject
from loguru import logger

from src.core.enums import PaymentGatewayType, SystemNotificationType, TransactionStatus
from src.core.utils.message_payload import MessagePayload
from src.core.utils.time import datetime_now
from src.infrastructure.taskiq.broker import broker
from src.services.notification import NotificationService
from src.services.payment_gateway import PaymentGatewayService
from src.services.transaction import TransactionService


@broker.task()
@inject
async def handle_payment_transaction_task(
    payment_id: UUID,
    payment_status: TransactionStatus,
    payment_gateway_service: FromDishka[PaymentGatewayService],
) -> None:
    match payment_status:
        case TransactionStatus.COMPLETED:
            await payment_gateway_service.handle_payment_succeeded(payment_id)
        case TransactionStatus.CANCELED:
            await payment_gateway_service.handle_payment_canceled(payment_id)


@broker.task(schedule=[{"cron": "*/10 * * * *"}])
@inject
async def notify_stuck_payments_task(
    transaction_service: FromDishka[TransactionService],
    notification_service: FromDishka[NotificationService],
) -> None:
    """Периодическая проверка зависших PENDING-платежей.

    Если есть PENDING-транзакции YooMoney старше 5 минут,
    отправляет уведомление администратору для ручной проверки.
    """
    transactions = await transaction_service.get_by_status(TransactionStatus.PENDING)
    if not transactions:
        return

    now = datetime_now()
    stuck = [
        tx for tx in transactions
        if tx.gateway_type == PaymentGatewayType.YOOMONEY
        and tx.created_at
        and now - tx.created_at > timedelta(minutes=5)
        and now - tx.created_at < timedelta(minutes=30)
    ]

    if not stuck:
        return

    tx_lines = []
    for tx in stuck:
        age_min = int((now - tx.created_at).total_seconds() // 60)  # type: ignore[operator]
        user_id = tx.user.telegram_id if tx.user else "?"
        tx_lines.append(
            f"• <code>{tx.payment_id}</code> — "
            f"{tx.pricing.final_amount} {tx.currency.symbol} — "
            f"user {user_id} — {age_min} мин. назад"
        )

    details = "\n".join(tx_lines)

    logger.warning(f"Found {len(stuck)} stuck YooMoney PENDING transactions")
    await notification_service.system_notify(
        payload=MessagePayload.not_deleted(
            i18n_key="ntf-event-stuck-payments",
            i18n_kwargs={
                "count": str(len(stuck)),
                "details": details,
            },
        ),
        ntf_type=SystemNotificationType.BILLING,
    )


@broker.task(schedule=[{"cron": "*/30 * * * *"}])
@inject
async def cancel_transaction_task(transaction_service: FromDishka[TransactionService]) -> None:
    transactions = await transaction_service.get_by_status(TransactionStatus.PENDING)

    if not transactions:
        logger.debug("No pending transactions found")
        return

    old_transactions = [tx for tx in transactions if tx.has_old]
    logger.debug(f"Found '{len(old_transactions)}' old transactions to cancel")

    for transaction in old_transactions:
        transaction.status = TransactionStatus.CANCELED
        await transaction_service.update(transaction)
        logger.debug(f"Transaction '{transaction.id}' canceled")
