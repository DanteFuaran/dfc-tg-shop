import asyncio
import time
from typing import Any, Union, cast

from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import BufferedInputFile
from dishka.integrations.taskiq import FromDishka, inject
from loguru import logger

from src.bot.keyboards import get_buy_keyboard, get_renew_keyboard
from src.core.constants import BATCH_DELAY, BATCH_SIZE
from src.core.enums import MediaType, UserNotificationType, SystemNotificationType
from src.core.storage.keys import CloseableMessagesKey
from src.core.utils.iterables import chunked
from src.core.utils.message_payload import MessagePayload
from src.core.utils.types import RemnaUserDto
from src.infrastructure.redis.repository import RedisRepository
from src.infrastructure.taskiq.broker import broker
from src.services.notification import NotificationService
from src.services.user import UserService


@broker.task
@inject
async def send_error_notification_task(
    error_id: Union[str, int],
    traceback_str: str,
    payload: MessagePayload,
    notification_service: FromDishka[NotificationService],
) -> None:
    file_data = BufferedInputFile(
        file=traceback_str.encode(),
        filename=f"error_{error_id}.txt",
    )
    payload.media = file_data
    payload.media_type = MediaType.DOCUMENT
    try:
        await notification_service.notify_super_dev(payload=payload)
    except TelegramRetryAfter as e:
        # Log rate limit, don't retry - prevent spam
        import logging
        logging.warning(f"Telegram rate limit on error notification, retry after {e.retry_after}s")


@broker.task
@inject
async def send_access_opened_notifications_task(
    waiting_user_ids: list[int],
    user_service: FromDishka[UserService],
    notification_service: FromDishka[NotificationService],
) -> None:
    for batch in chunked(waiting_user_ids, BATCH_SIZE):
        for user_telegram_id in batch:
            user = await user_service.get(user_telegram_id)
            await notification_service.notify_user(
                user=user,
                payload=MessagePayload(
                    i18n_key="ntf-access-allowed",
                    auto_delete_after=None,
                    add_close_button=True,
                ),
            )
        await asyncio.sleep(BATCH_DELAY)


@broker.task
@inject
async def send_payments_available_notifications_task(
    waiting_user_ids: list[int],
    user_service: FromDishka[UserService],
    notification_service: FromDishka[NotificationService],
) -> None:
    """Уведомление пользователей о том, что оплата сервиса снова доступна."""
    for batch in chunked(waiting_user_ids, BATCH_SIZE):
        for user_telegram_id in batch:
            user = await user_service.get(user_telegram_id)
            if user:
                await notification_service.notify_user(
                    user=user,
                    payload=MessagePayload(
                        i18n_key="ntf-payments-available-again",
                        auto_delete_after=None,
                        add_close_button=True,
                    ),
                )
        await asyncio.sleep(BATCH_DELAY)


@broker.task(retry_on_error=True)
@inject
async def send_subscription_expire_notification_task(
    remna_user: RemnaUserDto,
    ntf_type: UserNotificationType,
    i18n_kwargs: dict[str, Any],
    user_service: FromDishka[UserService],
    notification_service: FromDishka[NotificationService],
) -> None:
    telegram_id = cast(int, remna_user.telegram_id)
    i18n_kwargs_extra: dict[str, Any]

    if ntf_type == UserNotificationType.EXPIRES_IN_3_DAYS:
        i18n_key = "ntf-event-user-expiring"
        i18n_kwargs_extra = {"value": 3}
    elif ntf_type == UserNotificationType.EXPIRES_IN_2_DAYS:
        i18n_key = "ntf-event-user-expiring"
        i18n_kwargs_extra = {"value": 2}
    elif ntf_type == UserNotificationType.EXPIRES_IN_1_DAYS:
        i18n_key = "ntf-event-user-expiring"
        i18n_kwargs_extra = {"value": 1}
    elif ntf_type == UserNotificationType.EXPIRED:
        i18n_key = "ntf-event-user-expired"
        i18n_kwargs_extra = {}
    elif ntf_type == UserNotificationType.EXPIRED_1_DAY_AGO:
        i18n_key = "ntf-event-user-expired-ago"
        i18n_kwargs_extra = {"value": 1}
    else:
        logger.error(f"Unsupported notification type: {ntf_type}")
        return

    user = await user_service.get(telegram_id)

    if not user:
        raise ValueError(f"User '{telegram_id}' not found")

    if not user.current_subscription:
        logger.warning(f"Current subscription for user '{telegram_id}' not found, skipping notification")
        return

    i18n_kwargs_extra.update({"is_trial": user.current_subscription.is_trial})
    keyboard = get_buy_keyboard() if user.current_subscription.is_trial else get_renew_keyboard()

    await notification_service.notify_user(
        user=user,
        payload=MessagePayload(
            i18n_key=i18n_key,
            i18n_kwargs={**i18n_kwargs, **i18n_kwargs_extra},
            reply_markup=keyboard,
            auto_delete_after=None,
            add_close_button=True,
        ),
        ntf_type=ntf_type,
    )


@broker.task(retry_on_error=True)
@inject
async def send_subscription_limited_notification_task(
    remna_user: RemnaUserDto,
    i18n_kwargs: dict[str, Any],
    user_service: FromDishka[UserService],
    notification_service: FromDishka[NotificationService],
) -> None:
    telegram_id = cast(int, remna_user.telegram_id)
    user = await user_service.get(telegram_id)

    if not user:
        raise ValueError(f"User '{telegram_id}' not found")

    if not user.current_subscription:
        logger.warning(f"Current subscription for user '{telegram_id}' not found, skipping notification")
        return

    i18n_kwargs_extra = {
        "is_trial": user.current_subscription.is_trial,
        "traffic_strategy": user.current_subscription.traffic_limit_strategy,
        "reset_time": user.current_subscription.get_expire_time,
    }

    keyboard = get_buy_keyboard() if user.current_subscription.is_trial else get_renew_keyboard()

    await notification_service.notify_user(
        user=user,
        payload=MessagePayload(
            i18n_key="ntf-event-user-limited",
            i18n_kwargs={**i18n_kwargs, **i18n_kwargs_extra},
            reply_markup=keyboard,
            auto_delete_after=None,
            add_close_button=True,
        ),
        ntf_type=UserNotificationType.LIMITED,
    )

@broker.task(retry_on_error=True)
@inject
async def send_system_notification_task(
    ntf_type: SystemNotificationType,
    payload: MessagePayload,
    notification_service: FromDishka[NotificationService],
) -> None:
    await notification_service.system_notify(payload=payload, ntf_type=ntf_type)


@broker.task
@inject
async def send_delayed_transfer_notification_task(
    recipient_telegram_id: int,
    notification_text: str,
    delay_seconds: int,
    user_service: FromDishka[UserService],
    notification_service: FromDishka[NotificationService],
) -> None:
    """
    Отправляет уведомление о полученном переводе с задержкой.
    Это гарантирует что меню получателя уже обновлено к моменту отправки уведомления.
    """
    # Ждём указанное количество секунд
    await asyncio.sleep(delay_seconds)
    
    # Получаем актуальные данные пользователя
    recipient = await user_service.get(recipient_telegram_id)
    if not recipient:
        return
    
    # Отправляем уведомление
    await notification_service.notify_user(
        user=recipient,
        payload=MessagePayload(
            text=notification_text,
            add_close_button=True,
            auto_delete_after=None,
        ),
    )


# Auto-delete closeable messages older than 45 hours (before 48h Telegram limit)
_CLOSEABLE_MAX_AGE_SECONDS = 45 * 3600  # 45 hours


@broker.task(schedule=[{"cron": "0 * * * *"}])  # every hour
@inject
async def cleanup_closeable_messages_task(
    bot: FromDishka[Bot],
    redis_repository: FromDishka[RedisRepository],
) -> None:
    """Delete messages with 'Close' button that are older than 45 hours."""
    key = CloseableMessagesKey()
    cutoff = time.time() - _CLOSEABLE_MAX_AGE_SECONDS

    # Get all members with score (timestamp) <= cutoff
    expired: list[tuple[bytes, float]] = await redis_repository.client.zrangebyscore(
        key.pack(), "-inf", cutoff, withscores=True,
    )

    if not expired:
        return

    logger.info(f"[cleanup] Found {len(expired)} closeable messages older than 45h")

    deleted_count = 0
    failed_count = 0

    for raw_member, _score in expired:
        member = raw_member.decode() if isinstance(raw_member, bytes) else raw_member
        try:
            chat_id_str, message_id_str = member.split(":", 1)
            chat_id = int(chat_id_str)
            message_id = int(message_id_str)

            try:
                await bot.delete_message(chat_id=chat_id, message_id=message_id)
                deleted_count += 1
            except Exception:
                # Message already deleted by user or unavailable
                pass

            # Remove from sorted set regardless
            await redis_repository.sorted_collection_remove(key, member)
        except Exception as e:
            logger.error(f"[cleanup] Failed to process closeable message '{member}': {e}")
            # Remove broken entries
            await redis_repository.sorted_collection_remove(key, member)
            failed_count += 1

    logger.info(
        f"[cleanup] Closeable messages cleanup: deleted={deleted_count}, "
        f"failed={failed_count}, total={len(expired)}"
    )