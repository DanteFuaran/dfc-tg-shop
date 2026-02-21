from datetime import timedelta
from uuid import UUID

from dishka.integrations.taskiq import FromDishka, inject
from loguru import logger

from src.core.enums import PaymentGatewayType, TransactionStatus
from src.core.utils.time import datetime_now
from src.infrastructure.taskiq.broker import broker
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


@broker.task(schedule=[{"cron": "*/5 * * * *"}])
@inject
async def reconcile_yoomoney_task(
    payment_gateway_service: FromDishka[PaymentGatewayService],
    transaction_service: FromDishka[TransactionService],
) -> None:
    """Периодическая сверка PENDING-транзакций YooMoney.

    Проверяет через API operation-history, были ли получены платежи,
    вебхуки которых могли быть пропущены (например, при перезагрузке бота).
    """
    gateway_dto = await payment_gateway_service.get_by_type(PaymentGatewayType.YOOMONEY)
    if not gateway_dto or not gateway_dto.is_active:
        return

    from src.infrastructure.payment_gateways.yoomoney import YoomoneyGateway

    try:
        gateway = payment_gateway_service.payment_gateway_factory(gateway_dto)
    except Exception as exc:
        logger.warning(f"Failed to create YooMoney gateway instance: {exc}")
        return

    if not isinstance(gateway, YoomoneyGateway):
        logger.warning("YooMoney gateway factory returned unexpected type")
        return

    transactions = await transaction_service.get_by_status(TransactionStatus.PENDING)
    if not transactions:
        return

    now = datetime_now()
    yoomoney_pending = [
        tx for tx in transactions
        if tx.gateway_type == PaymentGatewayType.YOOMONEY
        and tx.created_at
        and now - tx.created_at > timedelta(minutes=2)
        and now - tx.created_at < timedelta(minutes=30)
    ]

    if not yoomoney_pending:
        return

    logger.info(f"YooMoney reconciliation: checking {len(yoomoney_pending)} pending transactions")

    for tx in yoomoney_pending:
        result = await gateway.check_payment_by_label(str(tx.payment_id))

        if result is None:
            logger.debug("YooMoney access_token not configured, skipping reconciliation")
            return

        if result is True:
            logger.info(
                f"YooMoney reconciliation: payment {tx.payment_id} confirmed, processing..."
            )
            await payment_gateway_service.handle_payment_succeeded(tx.payment_id)


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
