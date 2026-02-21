import asyncio
import html
from typing import Any

from aiogram import Bot, F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode, SubManager
from aiogram_dialog.widgets.kbd import Button, Select
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner
from loguru import logger

from remnapy.exceptions import NotFoundError as RemnaNotFoundError

from src.bot.keyboards import CALLBACK_CHANNEL_CONFIRM, CALLBACK_RULES_ACCEPT, get_user_keyboard
from src.bot.states import MainMenu, Subscription
from src.core.constants import USER_KEY
from src.core.enums import MediaType, PaymentGatewayType, PurchaseType, SubscriptionStatus, SystemNotificationType
from src.core.i18n.translator import get_translated_kwargs
from src.core.utils.adapter import DialogDataAdapter
from src.core.utils.formatters import (
    format_bytes_to_gb,
    format_user_log as log,
    i18n_format_days,
    i18n_format_device_limit,
    i18n_format_traffic_limit,
)
from src.core.utils.message_payload import MessagePayload
from src.infrastructure.database.models.dto import PlanSnapshotDto, SubscriptionDto, UserDto
from src.infrastructure.taskiq.tasks.redirects import redirect_to_main_menu_task
from src.infrastructure.taskiq.tasks.notifications import send_delayed_transfer_notification_task
from src.services.balance_transfer import BalanceTransferService
from src.services.extra_device import ExtraDeviceService
from src.services.notification import NotificationService
from src.services.payment_gateway import PaymentGatewayService
from src.services.plan import PlanService
from src.services.referral import ReferralService
from src.services.remnawave import RemnawaveService
from src.services.settings import SettingsService
from src.services.subscription import SubscriptionService
from src.services.user import UserService

router = Router(name=__name__)


@router.callback_query(F.data == "close_notification")
async def close_notification(callback: CallbackQuery) -> None:
    """Удаление уведомления по нажатию кнопки 'Закрыть'."""
    try:
        await callback.message.delete()
    except Exception:
        pass
    
    await callback.answer()


@router.callback_query(F.data == "close_success_transfer")
async def close_success_transfer(callback: CallbackQuery) -> None:
    """Удаление сообщения об успешном переводе по нажатию кнопки 'Готово'."""
    try:
        await callback.message.delete()
    except Exception:
        pass
    
    await callback.answer()


@router.callback_query(F.data == "close_subscription_key")
async def close_subscription_key(callback: CallbackQuery) -> None:
    """Удаление сообщения с ключом подписки по нажатию кнопки 'Закрыть'."""
    try:
        await callback.message.delete()
    except Exception:
        pass
    
    await callback.answer()


@inject
@router.message(F.text, StateFilter(MainMenu.BALANCE_AMOUNT))
async def validate_balance_amount_input(
    message: Message,
    dialog_manager: DialogManager,
    i18n: FromDishka[TranslatorRunner],
) -> None:
    """Validates balance amount before passing to dialog handler."""
    try:
        amount = int(message.text.strip())
        if amount < 5 or amount > 20000:
            raise ValueError("Amount out of range")
    except (ValueError, AttributeError):
        # Delete user message
        try:
            await message.delete()
        except Exception:
            pass
        
        # Show error notification (temporary message)
        error_msg = await message.answer(
            text=i18n.get("ntf-balance-invalid-amount"),
        )
        
        # Delete error message after 5 seconds
        try:
            import asyncio
            await asyncio.sleep(5)
            await error_msg.delete()
        except Exception:
            pass
        
        # Stop propagation to dialog handler
        return
    
    # If valid, let the dialog handler process it normally


async def on_start_dialog(
    user: UserDto,
    dialog_manager: DialogManager,
) -> None:
    logger.info(f"{log(user)} Started dialog")
    await dialog_manager.start(
        state=MainMenu.MAIN,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )


async def clear_chat_history(bot: Bot, chat_id: int, current_message_id: int) -> None:
    """Очищает историю чата, удаляя предыдущие сообщения."""
    deleted_count = 0
    # Пытаемся удалить до 100 предыдущих сообщений
    for offset in range(1, 101):
        try:
            await bot.delete_message(chat_id=chat_id, message_id=current_message_id - offset)
            deleted_count += 1
        except Exception:
            # Сообщение не существует или уже удалено
            continue
    
    if deleted_count > 0:
        logger.debug(f"Cleared {deleted_count} messages from chat {chat_id}")


@router.message(CommandStart(ignore_case=True))
async def on_start_command(
    message: Message,
    user: UserDto,
    dialog_manager: DialogManager,
) -> None:
    # Используем message.bot — это всегда тот бот, через которого пришло сообщение
    # (работает корректно и для основного бота, и для зеркальных)
    bot = message.bot
    asyncio.create_task(clear_chat_history(bot, message.chat.id, message.message_id))
    await on_start_dialog(user, dialog_manager)


@router.callback_query(F.data == CALLBACK_RULES_ACCEPT)
async def on_rules_accept(
    callback: CallbackQuery,
    user: UserDto,
    dialog_manager: DialogManager,
) -> None:
    logger.info(f"{log(user)} Accepted rules")
    await on_start_dialog(user, dialog_manager)


@router.callback_query(F.data == CALLBACK_CHANNEL_CONFIRM)
async def on_channel_confirm(
    callback: CallbackQuery,
    user: UserDto,
    dialog_manager: DialogManager,
) -> None:
    logger.info(f"{log(user)} Cofirmed join channel")
    await on_start_dialog(user, dialog_manager)


@inject
async def on_get_trial(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    plan_service: FromDishka[PlanService],
    user_service: FromDishka[UserService],
    referral_service: FromDishka[ReferralService],
    notification_service: FromDishka[NotificationService],
    remnawave_service: FromDishka[RemnawaveService],
    subscription_service: FromDishka[SubscriptionService],
) -> None:
    """
    Обработчик получения пробной подписки.
    Выполняет всё inline для мгновенного отклика (без taskiq очереди).
    """
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    
    logger.info(f"on_get_trial: User {user.telegram_id} clicked 'Get trial'")
    
    # 0. Проверяем, использовал ли пользователь уже пробную подписку
    has_used = await subscription_service.has_used_trial(user.telegram_id)
    if has_used:
        logger.warning(f"on_get_trial: User {user.telegram_id} already used trial subscription")
        await notification_service.notify_user(
            user=user,
            payload=MessagePayload(i18n_key="ntf-trial-already-used"),
        )
        return
    
    # 1. Очищаем кэш пользователя
    await user_service.clear_user_cache(user.telegram_id)
    
    # 2. ПРЯМАЯ ПРОВЕРКА в базе - есть ли реферал для этого пользователя
    referral = await referral_service.get_referral_by_referred(user.telegram_id)
    
    # 3. Получаем свежего пользователя (после очистки кэша)
    fresh_user = await user_service.get(user.telegram_id)
    if not fresh_user:
        logger.error(f"on_get_trial: User {user.telegram_id} not found after cache clear")
        await notification_service.notify_user(
            user=user,
            payload=MessagePayload(i18n_key="ntf-trial-unavailable"),
        )
        raise ValueError("User not found")
    
    # 4. КРИТИЧЕСКАЯ ПРОВЕРКА: если в базе есть реферал, но DTO говорит нет
    if referral and not fresh_user.is_invited_user:
        logger.warning(f"on_get_trial: User {user.telegram_id} has referral in DB but is_invited_user is FALSE")
        fresh_user._is_invited_user = True
    
    # 5. Получаем соответствующий пробный план
    is_invited = bool(referral)
    plan = await plan_service.get_appropriate_trial_plan(fresh_user, is_invited=is_invited)

    if not plan:
        logger.error(f"on_get_trial: No appropriate trial plan found for user {user.telegram_id}")
        await notification_service.notify_user(
            user=user,
            payload=MessagePayload(i18n_key="ntf-trial-unavailable"),
        )
        raise ValueError("Trial plan not exist")
    
    logger.info(f"on_get_trial: Selected plan - ID: {plan.id}, Name: '{plan.name}'")
    trial = PlanSnapshotDto.from_plan(plan, plan.durations[0].days)
    
    try:
        # ===== INLINE СОЗДАНИЕ ПОДПИСКИ (без taskiq) =====
        
        # Проверяем, существует ли пользователь в Remnawave
        existing_remna_user = None
        try:
            result = await remnawave_service.remnawave.users.get_users_by_telegram_id(
                telegram_id=str(user.telegram_id)
            )
            if result:
                existing_remna_user = result[0]
                logger.info(f"on_get_trial: Found existing user in Remnawave: uuid={existing_remna_user.uuid}")
        except RemnaNotFoundError:
            logger.debug(f"on_get_trial: No existing user in Remnawave for {user.telegram_id}")
        except Exception as e:
            logger.warning(f"on_get_trial: Error checking Remnawave user: {e}")
        
        # Если пользователь существует в Remnawave с активной подпиской
        if existing_remna_user and existing_remna_user.status in [SubscriptionStatus.ACTIVE, "ACTIVE"]:
            existing_tag = existing_remna_user.tag or "IMPORT"
            logger.info(f"on_get_trial: User has existing active subscription with tag '{existing_tag}'")
            
            # Пытаемся найти план по тегу
            matching_plan = await plan_service.get_by_tag(existing_tag)
            
            if matching_plan:
                # План найден - создаем подписку на основе существующего пользователя
                plan_snapshot = PlanSnapshotDto(
                    id=matching_plan.id,
                    name=matching_plan.name,
                    tag=matching_plan.tag,
                    type=matching_plan.type,
                    traffic_limit=matching_plan.traffic_limit,
                    device_limit=matching_plan.device_limit,
                    duration=matching_plan.duration,
                    traffic_limit_strategy=matching_plan.traffic_limit_strategy,
                    internal_squads=matching_plan.internal_squads,
                    external_squad=matching_plan.external_squad,
                )
                
                imported_subscription = SubscriptionDto(
                    user_remna_id=existing_remna_user.uuid,
                    status=existing_remna_user.status,
                    is_trial=False,
                    traffic_limit=format_bytes_to_gb(existing_remna_user.traffic_limit_bytes) if existing_remna_user.traffic_limit_bytes else matching_plan.traffic_limit,
                    device_limit=existing_remna_user.hwid_device_limit or matching_plan.device_limit,
                    traffic_limit_strategy=existing_remna_user.traffic_limit_strategy or matching_plan.traffic_limit_strategy,
                    tag=existing_tag,
                    internal_squads=matching_plan.internal_squads,
                    external_squad=matching_plan.external_squad,
                    expire_at=existing_remna_user.expire_at,
                    url=existing_remna_user.subscription_url,
                    plan=plan_snapshot,
                )
                
                await subscription_service.create(fresh_user, imported_subscription)
                logger.info(f"on_get_trial: Imported existing subscription for user '{user.telegram_id}'")
                
                await notification_service.notify_user(
                    user=fresh_user,
                    payload=MessagePayload(
                        i18n_key="ntf-existing-subscription-found",
                        i18n_kwargs={
                            "plan_name": matching_plan.name,
                            "tag": existing_tag,
                        },
                    ),
                )
            else:
                # План не найден - меняем тег на IMPORT
                logger.warning(f"on_get_trial: No matching plan for tag '{existing_tag}', changing to IMPORT")
                
                try:
                    from remnapy.models import UpdateUserRequestDto
                    await remnawave_service.remnawave.users.update_user(
                        UpdateUserRequestDto(
                            uuid=existing_remna_user.uuid,
                            tag="IMPORT",
                        )
                    )
                except Exception as e:
                    logger.error(f"on_get_trial: Failed to update tag to IMPORT: {e}")
                
                imported_subscription = SubscriptionDto(
                    user_remna_id=existing_remna_user.uuid,
                    status=existing_remna_user.status,
                    is_trial=False,
                    traffic_limit=format_bytes_to_gb(existing_remna_user.traffic_limit_bytes) if existing_remna_user.traffic_limit_bytes else 0,
                    device_limit=existing_remna_user.hwid_device_limit or 1,
                    traffic_limit_strategy=existing_remna_user.traffic_limit_strategy,
                    tag="IMPORT",
                    internal_squads=[],
                    external_squad=None,
                    expire_at=existing_remna_user.expire_at,
                    url=existing_remna_user.subscription_url,
                    plan=None,
                )
                
                await subscription_service.create(fresh_user, imported_subscription)
                
                await notification_service.notify_user(
                    user=fresh_user,
                    payload=MessagePayload(
                        i18n_key="ntf-existing-subscription-no-plan",
                        i18n_kwargs={"old_tag": existing_tag},
                    ),
                )
        else:
            # Пользователя нет в Remnawave или подписка неактивна - создаём пробную
            created_remna_user = await remnawave_service.create_user(fresh_user, plan=trial, force=True)
            
            trial_subscription = SubscriptionDto(
                user_remna_id=created_remna_user.uuid,
                status=created_remna_user.status,
                is_trial=True,
                traffic_limit=trial.traffic_limit,
                device_limit=trial.device_limit,
                traffic_limit_strategy=trial.traffic_limit_strategy,
                tag=trial.tag,
                internal_squads=trial.internal_squads,
                external_squad=trial.external_squad,
                expire_at=created_remna_user.expire_at,
                url=created_remna_user.subscription_url,
                plan=trial,
            )
            
            await subscription_service.create(fresh_user, trial_subscription)
            logger.info(f"on_get_trial: Created new trial subscription for user '{user.telegram_id}'")
            
            # Системное уведомление для админов
            await notification_service.system_notify(
                ntf_type=SystemNotificationType.TRIAL_GETTED,
                payload=MessagePayload.not_deleted(
                    i18n_key="ntf-event-subscription-trial",
                    i18n_kwargs={
                        "user_id": str(user.telegram_id),
                        "user_name": user.name,
                        "username": user.username or False,
                        "plan_name": trial.name,
                        "plan_type": trial.type,
                        "plan_traffic_limit": i18n_format_traffic_limit(trial.traffic_limit),
                        "plan_device_limit": i18n_format_device_limit(trial.device_limit),
                        "plan_duration": i18n_format_days(trial.duration),
                        "plan_price": "0 ₽",
                    },
                    reply_markup=get_user_keyboard(user.telegram_id),
                ),
            )
        
        # ===== МГНОВЕННЫЙ ПЕРЕХОД (вместо taskiq redirect) =====
        # Очищаем кеш пользователя чтобы getter_connect увидел новую подписку
        await user_service.clear_user_cache(fresh_user.telegram_id)
        
        # Даём время на загрузку данных в кеш
        import asyncio
        await asyncio.sleep(0.5)
        
        # Дополнительная проверка - загружаем пользователя снова и убеждаемся что подписка есть
        verify_user = await user_service.get(fresh_user.telegram_id)
        if not verify_user or not verify_user.current_subscription:
            logger.error(f"on_get_trial: Subscription not found after creation for user {user.telegram_id}, retrying...")
            await asyncio.sleep(1)
            # Попытка 2
            await user_service.clear_user_cache(fresh_user.telegram_id)
            verify_user = await user_service.get(fresh_user.telegram_id)
        
        await dialog_manager.start(
            state=Subscription.TRIAL,
            mode=StartMode.RESET_STACK,
            show_mode=ShowMode.DELETE_AND_SEND,
        )
        logger.info(f"on_get_trial: Successfully completed for user {user.telegram_id}")
        
    except Exception as e:
        logger.exception(f"on_get_trial: Failed for user {user.telegram_id}: {e}")
        await notification_service.notify_user(
            user=fresh_user,
            payload=MessagePayload(i18n_key="ntf-trial-unavailable"),
        )
        raise


@inject
async def on_device_delete(
    callback: CallbackQuery,
    widget: Button,
    sub_manager: SubManager,
    remnawave_service: FromDishka[RemnawaveService],
    extra_device_service: FromDishka[ExtraDeviceService],
    subscription_service: FromDishka[SubscriptionService],
    user_service: FromDishka[UserService],
    notification_service: FromDishka[NotificationService],
    i18n: FromDishka[TranslatorRunner],
) -> None:
    """Удаление устройства или пометка extra слота на удаление."""
    import time
    import asyncio
    
    await sub_manager.load_data()
    slot_id = sub_manager.item_id  # Получаем индекс слота
    user: UserDto = sub_manager.middleware_data[USER_KEY]
    
    # Получаем маппинги из dialog_data
    slot_hwid_map = sub_manager.dialog_data.get("slot_hwid_map", {})
    slot_purchase_map = sub_manager.dialog_data.get("slot_purchase_map", {})
    hwid_map = sub_manager.dialog_data.get("hwid_map")
    
    # Проверяем, это занятый слот (есть hwid) или пустой extra слот (есть purchase_id)
    selected_short_hwid = slot_hwid_map.get(slot_id)
    purchase_id = slot_purchase_map.get(slot_id)
    
    # Если это extra слот (есть purchase_id) - используем отложенное удаление
    if purchase_id:
        # Получаем информацию о покупке
        purchase = await extra_device_service.get(purchase_id)
        if not purchase:
            return
        
        # Проверяем подтверждение удаления
        pending_delete = sub_manager.dialog_data.get("pending_delete_slot")
        pending_timestamp = sub_manager.dialog_data.get("pending_delete_timestamp")
        
        # Проверяем, это повторное нажатие в течение 5 секунд
        is_confirmed = (
            pending_delete == slot_id 
            and pending_timestamp is not None
            and time.time() - pending_timestamp < 5
        )
        
        if not is_confirmed:
            # Первое нажатие - отправляем предупреждение
            sub_manager.dialog_data["pending_delete_slot"] = slot_id
            sub_manager.dialog_data["pending_delete_timestamp"] = time.time()
            
            # Получаем переведённое сообщение
            warning_text = i18n.get("msg-device-deletion-warning")
            
            warning_msg = await callback.message.answer(warning_text)
            
            # Сохраняем ID сообщения для последующего удаления
            sub_manager.dialog_data["warning_message_id"] = warning_msg.message_id
            
            # Удаляем сообщение через 5 секунд
            async def delete_warning():
                await asyncio.sleep(5)
                try:
                    await warning_msg.delete()
                except Exception:
                    pass
            
            asyncio.create_task(delete_warning())
            await callback.answer()
            return
        
        # Подтверждено - уменьшаем количество устройств на 1
        sub_manager.dialog_data.pop("pending_delete_slot", None)
        sub_manager.dialog_data.pop("pending_delete_timestamp", None)
        
        # Удаляем warning сообщение сразу
        warning_message_id = sub_manager.dialog_data.pop("warning_message_id", None)
        if warning_message_id:
            try:
                await callback.bot.delete_message(
                    chat_id=callback.message.chat.id,
                    message_id=warning_message_id
                )
            except Exception:
                pass
        
        # Помечаем покупку на удаление (теперь каждая покупка = 1 устройство)
        await extra_device_service.mark_for_deletion(purchase_id)
        logger.info(
            f"{log(user)} Marked extra device purchase '{purchase_id}' for deletion "
            f"(will be removed after {purchase.expires_at})"
        )
        
        # Очищаем кеш
        await user_service.clear_user_cache(user.telegram_id)
        
        # Рассчитываем время до удаления
        from src.core.utils.time import datetime_now
        from datetime import timedelta
        time_until_delete = purchase.expires_at - datetime_now()
        days = time_until_delete.days
        hours = time_until_delete.seconds // 3600
        
        if days > 0:
            delete_after = f"{days} дн. {hours} ч."
        elif hours > 0:
            delete_after = f"{hours} ч."
        else:
            delete_after = "менее часа"
        
        # Уведомляем разработчика об удалении (Event-уведомление)
        from src.core.enums import SystemNotificationType
        from src.bot.keyboards import get_user_keyboard
        await notification_service.system_notify(
            payload=MessagePayload.not_deleted(
                i18n_key="ntf-event-extra-devices-deletion",
                i18n_kwargs={
                    "user_id": str(user.telegram_id),
                    "user_name": user.name,
                    "username": user.username or False,
                    "device_count": 1,
                    "delete_after": delete_after,
                },
                reply_markup=get_user_keyboard(user.telegram_id),
            ),
            ntf_type=SystemNotificationType.EXTRA_DEVICES,
        )
        
        await notification_service.notify_user(
            user=user,
            payload=MessagePayload(i18n_key="ntf-extra-device-marked-deletion"),
        )
        
        # Получаем переведённый ответ
        await callback.answer(i18n.get("btn-device-marked-for-deletion"))
        
        # Обновляем диалог чтобы отобразить изменения
        from aiogram_dialog import ShowMode
        await sub_manager.update({}, show_mode=ShowMode.EDIT)
        return
    
    elif selected_short_hwid:
        # Удаляем устройство из базового/бонусного слота
        if not hwid_map:
            raise ValueError(f"Selected '{selected_short_hwid}' HWID, but 'hwid_map' is missing")

        full_hwid = next((d["hwid"] for d in hwid_map if d["short_hwid"] == selected_short_hwid), None)

        if not full_hwid:
            raise ValueError(f"Full HWID not found for '{selected_short_hwid}'")

        if not (user.current_subscription and user.current_subscription.device_limit):
            raise ValueError("User has no active subscription or device limit unlimited")

        devices = await remnawave_service.delete_device(user=user, hwid=full_hwid)
        logger.info(f"{log(user)} Deleted device '{full_hwid}'")

        # Показываем уведомление об успешном удалении устройства
        await notification_service.notify_user(
            user=user,
            payload=MessagePayload(i18n_key="ntf-device-deleted"),
        )
        return
    
    else:
        raise ValueError(f"Slot '{slot_id}' has no hwid or purchase_id")


@inject
async def on_pending_deletion_info(
    callback: CallbackQuery,
    widget: Button,
    sub_manager: SubManager,
    remnawave_service: FromDishka[RemnawaveService],
    notification_service: FromDishka[NotificationService],
) -> None:
    """Удалить устройство из слота на удалении."""
    await sub_manager.load_data()
    slot_id = sub_manager.item_id
    user: UserDto = sub_manager.middleware_data[USER_KEY]
    
    # Получаем маппинги из dialog_data
    slot_hwid_map = sub_manager.dialog_data.get("slot_hwid_map", {})
    hwid_map = sub_manager.dialog_data.get("hwid_map")
    
    # Проверяем, есть ли устройство в этом слоте
    selected_short_hwid = slot_hwid_map.get(slot_id)
    
    if not selected_short_hwid:
        # Слот пустой - ничего не делаем
        await callback.answer("Слот пустой", show_alert=False)
        return
    
    # Удаляем устройство из слота
    if not hwid_map:
        raise ValueError(f"Selected '{selected_short_hwid}' HWID, but 'hwid_map' is missing")

    full_hwid = next((d["hwid"] for d in hwid_map if d["short_hwid"] == selected_short_hwid), None)

    if not full_hwid:
        raise ValueError(f"Full HWID not found for '{selected_short_hwid}'")

    if not (user.current_subscription and user.current_subscription.device_limit):
        raise ValueError("User has no active subscription or device limit unlimited")

    devices = await remnawave_service.delete_device(user=user, hwid=full_hwid)
    logger.info(f"{log(user)} Deleted device '{full_hwid}' from pending deletion slot")

    # Показываем уведомление об успешном удалении устройства
    await notification_service.notify_user(
        user=user,
        payload=MessagePayload(i18n_key="ntf-device-deleted"),
    )


@inject
async def show_reason(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    i18n: FromDishka[TranslatorRunner],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    subscription = user.current_subscription

    if subscription:
        kwargs = {
            "status": subscription.get_status,
            "is_trial": subscription.is_trial,
            "traffic_strategy": subscription.traffic_limit_strategy,
            "reset_time": subscription.get_expire_time,
        }
    else:
        kwargs = {"status": False}

    await callback.answer(
        text=i18n.get("ntf-connect-not-available", **get_translated_kwargs(i18n, kwargs)),
        show_alert=True,
    )


@inject
async def on_connect_app(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    bot: FromDishka[Bot],
) -> None:
    """Обработчик для добавления подписки в приложение Happ."""
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    subscription = user.current_subscription
    
    if not subscription:
        await callback.answer(
            text="❌ У вас нет активной подписки.",
            show_alert=True,
        )
        return
    
    # Формируем ссылку для открытия через WebApp
    happ_add_url = f"happ://add/{subscription.url}"
    
    # Пытаемся открыть ссылку
    await callback.answer()
    
    # Отправляем сообщение с инструкцией
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=f"📱 Откройте приложение Happ и добавьте подписку:\n\n<code>{happ_add_url}</code>",
        parse_mode="HTML"
    )


@inject
async def on_show_qr(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    referral_service: FromDishka[ReferralService],
    notification_service: FromDishka[NotificationService],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]

    ref_link = await referral_service.get_ref_link(user.referral_code)
    ref_qr = referral_service.get_ref_qr(ref_link)

    # Send QR code as a separate message without closing the dialog
    await notification_service.notify_user(
        user=user,
        payload=MessagePayload.not_deleted(
            i18n_key="",
            media=ref_qr,
            media_type=MediaType.PHOTO,
            close_button_style="success",
        ),
    )


@inject
async def on_show_key(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    notification_service: FromDishka[NotificationService],
    i18n: FromDishka[TranslatorRunner],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    
    subscription = user.current_subscription
    if not subscription:
        return
    
    subscription_url = subscription.url if subscription.url else ""
    if not subscription_url:
        return
    
    # Create message text using i18n
    message_text = (
        f"{i18n.get('msg-subscription-key-title')}\n\n"
        f"<pre>{subscription_url}</pre>"
    )
    
    # Create close button
    close_button = InlineKeyboardButton(
        text=i18n.get("btn-notification-close-success"),
        callback_data="close_subscription_key",
        style="success",
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[close_button]])
    
    # Send subscription URL message with close button
    try:
        await callback.bot.send_message(
            chat_id=callback.from_user.id,
            text=message_text,
            parse_mode="HTML",
            reply_markup=keyboard,
        )
    except Exception:
        pass


@inject
async def on_withdraw_points(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    i18n: FromDishka[TranslatorRunner],
    referral_service: FromDishka[ReferralService],
    user_service: FromDishka[UserService],
    notification_service: FromDishka[NotificationService],
) -> None:
    from src.core.enums import ReferralRewardType
    
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    
    # Get pending referral balance
    pending_amount = await referral_service.get_pending_rewards_amount(
        user.telegram_id,
        ReferralRewardType.MONEY,
    )
    
    if pending_amount <= 0:
        # Send temporary error message instead of popup
        try:
            error_msg = await callback.bot.send_message(
                chat_id=callback.from_user.id,
                text=i18n.get("ntf-invite-withdraw-no-balance"),
            )
            # Delete message after 5 seconds
            await asyncio.sleep(5)
            await error_msg.delete()
        except Exception:
            pass
        
        return
    
    # Withdraw rewards (mark as issued)
    withdrawn_amount = await referral_service.withdraw_pending_rewards(
        user.telegram_id,
        ReferralRewardType.MONEY,
    )
    
    # Add to user balance
    await user_service.add_to_balance(user, withdrawn_amount)
    
    # Обновляем баланс пользователя в middleware_data, чтобы окно отобразило новый баланс
    user.balance += withdrawn_amount
    dialog_manager.middleware_data[USER_KEY] = user
    
    # Refresh the dialog to show updated balance
    await dialog_manager.show()
    
    # Send temporary success message AFTER refresh
    try:
        success_msg = await callback.bot.send_message(
            chat_id=callback.from_user.id,
            text=i18n.get("ntf-invite-withdraw-success", amount=withdrawn_amount),
        )
        # Delete message after 5 seconds
        await asyncio.sleep(5)
        await success_msg.delete()
    except Exception:
        pass


@inject
async def on_invite(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    settings_service: FromDishka[SettingsService],
) -> None:
    if await settings_service.is_referral_enable():
        await dialog_manager.switch_to(state=MainMenu.INVITE)
    else:
        return


async def on_promocode(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    """Переход к окну ввода промокода."""
    await dialog_manager.start(state=Subscription.PROMOCODE, mode=StartMode.NORMAL)


async def on_platform_select(
    callback: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
) -> None:
    """Обработчик выбора платформы для скачивания."""
    dialog_manager.dialog_data["selected_platform"] = item_id


@inject
async def on_balance_click(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    payment_gateway_service: FromDishka[PaymentGatewayService],
    notification_service: FromDishka[NotificationService],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    logger.info(f"{log(user)} Opened balance topup")

    gateways = await payment_gateway_service.filter_active()

    if not gateways:
        logger.warning(f"{log(user)} No active payment gateways for topup")
        await notification_service.notify_user(
            user=user,
            payload=MessagePayload(i18n_key="ntf-subscription-gateways-not-available"),
        )
        return

    # Navigate to balance payment method selection
    await dialog_manager.switch_to(state=MainMenu.BALANCE)


@inject
async def on_balance_gateway_select(
    callback: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
    item_id: str,
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    gateway_type = PaymentGatewayType(item_id)
    
    logger.info(f"{log(user)} Selected payment gateway '{gateway_type}' for balance topup")
    
    dialog_manager.dialog_data["selected_gateway"] = gateway_type
    await dialog_manager.switch_to(state=MainMenu.BALANCE_AMOUNTS)


@inject
async def on_balance_amount_select(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    payment_gateway_service: FromDishka[PaymentGatewayService],
    notification_service: FromDishka[NotificationService],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    
    # Extract amount from button id (e.g., "amount_100" -> 100)
    amount = int(widget.widget_id.split("_")[1])
    
    gateway_type_raw = dialog_manager.dialog_data.get("selected_gateway")
    
    # Конвертируем строку в enum если нужно
    if isinstance(gateway_type_raw, str):
        gateway_type = PaymentGatewayType(gateway_type_raw)
    else:
        gateway_type = gateway_type_raw
    
    if not gateway_type:
        await notification_service.notify_user(
            user=user,
            payload=MessagePayload(i18n_key="ntf-subscription-gateways-not-available"),
        )
        return
    
    logger.info(f"{log(user)} Selected preset amount '{amount}' for balance topup via '{gateway_type}'")
    
    # Create payment for balance topup
    gateway = await payment_gateway_service.get_by_type(gateway_type)
    if not gateway:
        await notification_service.notify_user(
            user=user,
            payload=MessagePayload(i18n_key="ntf-subscription-gateways-not-available"),
        )
        return
    
    # Create payment immediately
    try:
        payment_result = await payment_gateway_service.create_topup_payment(
            user=user,
            amount=amount,
            gateway_type=gateway_type,
        )
        
        if not payment_result.url:
            await payment_gateway_service.handle_payment_succeeded(payment_result.id)
            await notification_service.notify_user(
                user=user,
                payload=MessagePayload(i18n_key="ntf-balance-topup-success"),
            )
            return
        
        # Store payment data and proceed to confirmation
        dialog_manager.dialog_data["topup_amount"] = amount
        dialog_manager.dialog_data["currency"] = gateway.currency
        dialog_manager.dialog_data["payment_url"] = payment_result.url
        dialog_manager.dialog_data["payment_id"] = str(payment_result.id)
        
        logger.info(f"{log(user)} Payment created: {payment_result.url}")
        await dialog_manager.switch_to(state=MainMenu.BALANCE_CONFIRM, show_mode=ShowMode.EDIT)
        
    except Exception as e:
        logger.error(f"{log(user)} Failed to create topup payment: {e}")
        await notification_service.notify_user(
            user=user,
            payload=MessagePayload(i18n_key="ntf-subscription-payment-creation-failed"),
        )


@inject
async def on_balance_amount_input(
    message: Message,
    widget: Any,
    dialog_manager: DialogManager,
    payment_gateway_service: FromDishka[PaymentGatewayService],
    notification_service: FromDishka[NotificationService],
    settings_service: FromDishka[SettingsService],
    i18n: FromDishka[TranslatorRunner],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    
    # Получаем настройки min/max для пополнения баланса
    settings = await settings_service.get()
    min_amount = settings.features.balance_min_amount if settings.features.balance_min_amount is not None else 10
    max_amount = settings.features.balance_max_amount if settings.features.balance_max_amount is not None else 100000
    
    # Validate amount
    try:
        amount = int(message.text.strip())
        if amount < min_amount or amount > max_amount:
            raise ValueError("Amount out of range")
    except (ValueError, AttributeError):
        # Delete user message
        try:
            await message.delete()
        except Exception:
            pass
        
        # Show error notification (temporary message)
        error_msg = await message.answer(
            text=i18n.get("ntf-balance-invalid-amount", min_amount=min_amount, max_amount=max_amount),
        )
        
        # Delete error message after 5 seconds in background task
        import asyncio
        async def delete_after_delay():
            await asyncio.sleep(5)
            try:
                await error_msg.delete()
            except Exception:
                pass
        
        asyncio.create_task(delete_after_delay())
        
        # Prevent dialog from re-rendering by setting show mode
        dialog_manager.show_mode = ShowMode.NO_UPDATE
        return
    
    # Удаляем сообщение пользователя для плавного перехода
    try:
        await message.delete()
    except Exception:
        pass
    
    gateway_type_raw = dialog_manager.dialog_data.get("selected_gateway")
    
    # Конвертируем строку в enum если нужно
    if isinstance(gateway_type_raw, str):
        gateway_type = PaymentGatewayType(gateway_type_raw)
    else:
        gateway_type = gateway_type_raw
    
    if not gateway_type:
        await notification_service.notify_user(
            user=user,
            payload=MessagePayload(i18n_key="ntf-subscription-gateways-not-available"),
        )
        return
    
    logger.info(f"{log(user)} Entered amount '{amount}' for balance topup via '{gateway_type}'")
    
    # Create payment for balance topup
    gateway = await payment_gateway_service.get_by_type(gateway_type)
    if not gateway:
        await notification_service.notify_user(
            user=user,
            payload=MessagePayload(i18n_key="ntf-subscription-gateways-not-available"),
        )
        return
    
    # Create payment immediately
    try:
        payment_result = await payment_gateway_service.create_topup_payment(
            user=user,
            amount=amount,
            gateway_type=gateway_type,
        )
        
        if not payment_result.url:
            # Free payment (shouldn't happen for topup, but handle it)
            await payment_gateway_service.handle_payment_succeeded(payment_result.id)
            await notification_service.notify_user(
                user=user,
                payload=MessagePayload(i18n_key="ntf-balance-topup-success"),
            )
            return
        
        # Store payment data and proceed to confirmation
        dialog_manager.dialog_data["topup_amount"] = amount
        dialog_manager.dialog_data["currency"] = gateway.currency
        dialog_manager.dialog_data["payment_url"] = payment_result.url
        dialog_manager.dialog_data["payment_id"] = str(payment_result.id)
        
        logger.info(f"{log(user)} Payment created: {payment_result.url}")
        await dialog_manager.switch_to(state=MainMenu.BALANCE_CONFIRM, show_mode=ShowMode.EDIT)
        
    except Exception as e:
        logger.error(f"{log(user)} Failed to create topup payment: {e}")
        await notification_service.notify_user(
            user=user,
            payload=MessagePayload(i18n_key="ntf-subscription-payment-creation-failed"),
        )


@inject
async def on_balance_withdraw_click(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    i18n: FromDishka[TranslatorRunner],
) -> None:
    await callback.answer(
        text=i18n.get("ntf-balance-withdraw-in-development"),
        show_alert=True,
    )


async def on_bonus_amount_select(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    """Сохранить выбранную сумму бонусов в dialog_data (только выбор, без зачисления)."""
    # Получаем выбранную сумму из callback.data
    amount_str = callback.data.split("_")[-1]
    
    # Ответим на callback
    await callback.answer()
    
    # Сохраняем выбор
    dialog_manager.dialog_data["pending_bonus_amount"] = amount_str


@inject
async def on_accept_bonus_amount(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    user_service: FromDishka[UserService],
    referral_service: FromDishka[ReferralService],
    i18n: FromDishka[TranslatorRunner],
) -> None:
    """Применить выбранную сумму бонусов при нажатии Принять."""
    from src.core.enums import ReferralRewardType
    from src.core.constants import USER_KEY
    import asyncio
    
    pending_amount_str = dialog_manager.dialog_data.get("pending_bonus_amount")
    
    if not pending_amount_str:
        await callback.answer(
            text=i18n.get("ntf-bonus-activate-no-selection"),
            show_alert=True,
        )
        return
    
    # Ответим на callback ДО асинхронных операций
    await callback.answer()
    
    # Получаем доступный баланс
    available_balance = await referral_service.get_pending_rewards_amount(
        callback.from_user.id,
        ReferralRewardType.MONEY,
    )
    
    if pending_amount_str == "all":
        amount = available_balance
    else:
        amount = int(pending_amount_str)
    
    # Проверяем, достаточно ли бонусов
    if amount > available_balance or amount <= 0:
        # Отправляем уведомление как сообщение
        error_msg = await callback.bot.send_message(
            chat_id=callback.from_user.id,
            text=i18n.get("ntf-bonus-insufficient"),
        )
        
        # Удаляем сообщение через 5 секунд в фоне
        async def delete_error():
            try:
                await asyncio.sleep(5)
                await callback.bot.delete_message(
                    chat_id=callback.from_user.id,
                    message_id=error_msg.message_id,
                )
            except Exception:
                pass
        
        asyncio.create_task(delete_error())
        return
    
    # Получаем пользователя
    user = dialog_manager.middleware_data[USER_KEY]
    
    try:
        # Зачисляем только выбранную сумму бонусов на основной баланс
        await referral_service.withdraw_pending_rewards(
            user.telegram_id,
            ReferralRewardType.MONEY,
            amount=amount,
        )
        
        # Добавляем на основной баланс
        await user_service.add_to_balance(user, amount)
        
        # Обновляем данные пользователя в middleware
        user.balance += amount
        dialog_manager.middleware_data[USER_KEY] = user
        
        # Очищаем данные диалога
        dialog_manager.dialog_data.pop("pending_bonus_amount", None)
        
        # Возвращаемся в меню баланса
        await dialog_manager.switch_to(MainMenu.BALANCE)
        
        # Отправляем уведомление об успехе в фоне (без блокировки)
        async def send_notification():
            try:
                success_msg = await callback.bot.send_message(
                    chat_id=callback.from_user.id,
                    text=i18n.get("ntf-bonus-activated", amount=amount),
                )
                await asyncio.sleep(5)
                await callback.bot.delete_message(
                    chat_id=callback.from_user.id,
                    message_id=success_msg.message_id,
                )
            except Exception:
                pass
        
        asyncio.create_task(send_notification())
            
    except Exception as e:
        logger.error(f"{log(user)} Failed to activate bonus: {e}")
        await callback.answer(
            text=i18n.get("ntf-bonus-activate-failed"),
            show_alert=True,
        )


async def on_bonus_custom_mode(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    """Переключиться в режим ручного ввода суммы бонусов."""
    # Сохраняем ID текущего сообщения диалога для последующего удаления
    if callback.message:
        dialog_manager.dialog_data["dialog_window_message_id"] = callback.message.message_id
    await dialog_manager.switch_to(MainMenu.BONUS_ACTIVATE_CUSTOM)





@inject
async def on_cancel_bonus_amount(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    """Отменить меню активации бонусов и вернуться в меню баланса."""
    dialog_manager.dialog_data.pop("pending_bonus_amount", None)
    await dialog_manager.switch_to(MainMenu.BALANCE)


@inject
async def on_bonus_custom_input(
    message: Message,
    widget: Any,
    dialog_manager: DialogManager,
    referral_service: FromDishka[ReferralService],
    i18n: FromDishka[TranslatorRunner],
    user: UserDto,
    **kwargs: Any,
) -> None:
    """Сохранить пользовательскую сумму бонусов в dialog_data."""
    from src.core.enums import ReferralRewardType
    
    try:
        amount = int(message.text)
        
        if amount <= 0:
            await message.answer(i18n.get("ntf-bonus-invalid-amount"))
            return
        
        # Get available balance
        available = await referral_service.get_pending_rewards_amount(
            user.telegram_id,
            ReferralRewardType.MONEY,
        )
        
        if amount > available:
            await message.answer(
                i18n.get("ntf-bonus-amount-exceeds", available=available)
            )
            return
        
        # Save to dialog_data
        dialog_manager.dialog_data["pending_bonus_amount"] = amount
        
        # Delete input message
        try:
            await message.delete()
        except Exception as e:
            logger.debug(f"Failed to delete message: {e}")
        
        # Go back to bonus activate menu
        await dialog_manager.switch_to(MainMenu.BONUS_ACTIVATE)
            
    except ValueError:
        await message.answer(i18n.get("ntf-bonus-invalid-format"))
    except Exception as e:
        logger.error(f"{log(user)} Failed to process custom bonus: {e}")
        await message.answer(i18n.get("ntf-bonus-activate-failed"))


# === Balance Transfer Handlers ===


@inject
async def on_balance_transfer_click(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    settings_service: FromDishka[SettingsService],
    i18n: FromDishka[TranslatorRunner],
) -> None:
    """Нажатие на кнопку перевода - проверяем включена ли функция."""
    settings = await settings_service.get()
    
    if not settings.features.transfers.enabled:
        await callback.answer(
            text=i18n.get("ntf-balance-transfer-disabled"),
            show_alert=True,
        )
        return
    
    # Инициализируем transfer_data если его нет
    if "transfer_data" not in dialog_manager.dialog_data:
        dialog_manager.dialog_data["transfer_data"] = {}
    
    await dialog_manager.switch_to(MainMenu.BALANCE_TRANSFER)


async def on_balance_transfer_recipient_click(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    """Открытие окна ввода получателя."""
    await dialog_manager.switch_to(MainMenu.BALANCE_TRANSFER_RECIPIENT)


@inject
async def on_balance_transfer_recipient_input(
    message: Message,
    widget: Any,
    dialog_manager: DialogManager,
    user_service: FromDishka[UserService],
    i18n: FromDishka[TranslatorRunner],
) -> None:
    """Обработка ввода ID получателя."""
    dialog_manager.show_mode = ShowMode.EDIT
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    
    recipient_input = message.text.strip()
    
    # Проверяем что введен числовой ID
    if not recipient_input.isdigit():
        error_msg = await message.answer(
            text=i18n.get("ntf-balance-transfer-invalid-id"),
        )
        await asyncio.sleep(5)
        try:
            await error_msg.delete()
        except Exception:
            pass
        try:
            await message.delete()
        except Exception:
            pass
        return
    
    # Ищем пользователя по telegram_id
    recipient = await user_service.get(int(recipient_input))
    
    if not recipient:
        error_msg = await message.answer(
            text=i18n.get("ntf-balance-transfer-user-not-found"),
        )
        await asyncio.sleep(5)
        try:
            await error_msg.delete()
        except Exception:
            pass
        try:
            await message.delete()
        except Exception:
            pass
        return
    
    # Проверяем что пользователь не переводит самому себе
    if recipient.telegram_id == user.telegram_id:
        error_msg = await message.answer(
            text=i18n.get("ntf-balance-transfer-self"),
        )
        await asyncio.sleep(5)
        try:
            await error_msg.delete()
        except Exception:
            pass
        try:
            await message.delete()
        except Exception:
            pass
        return
    
    # Сохраняем получателя в transfer_data
    if "transfer_data" not in dialog_manager.dialog_data:
        dialog_manager.dialog_data["transfer_data"] = {}
    
    dialog_manager.dialog_data["transfer_data"]["recipient_id"] = recipient.telegram_id
    dialog_manager.dialog_data["transfer_data"]["recipient_name"] = recipient.name or f"ID: {recipient.telegram_id}"
    
    # Возвращаемся в главное окно перевода
    await dialog_manager.switch_to(MainMenu.BALANCE_TRANSFER)
    
    try:
        await message.delete()
    except Exception:
        pass


async def on_balance_transfer_recipient_cancel(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    """Отмена ввода получателя."""
    await dialog_manager.switch_to(MainMenu.BALANCE_TRANSFER)


async def on_balance_transfer_recipient_history_click(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    """Открытие окна истории получателей переводов."""
    await dialog_manager.switch_to(MainMenu.BALANCE_TRANSFER_RECIPIENT_HISTORY)


async def on_balance_transfer_recipient_history_select(
    callback: CallbackQuery,
    widget: Select[int],
    dialog_manager: DialogManager,
    selected_user: int,
) -> None:
    """Выбор получателя из истории переводов."""
    from src.services.user import UserService
    from dishka.integrations.aiogram_dialog import inject
    
    # Получаем user_service из контейнера через middleware_data
    container = dialog_manager.middleware_data.get("dishka_container")
    if container:
        user_service = await container.get(UserService)
        recipient = await user_service.get(selected_user)
        
        if recipient:
            if "transfer_data" not in dialog_manager.dialog_data:
                dialog_manager.dialog_data["transfer_data"] = {}
            
            dialog_manager.dialog_data["transfer_data"]["recipient_id"] = recipient.telegram_id
            dialog_manager.dialog_data["transfer_data"]["recipient_name"] = recipient.name or f"ID: {recipient.telegram_id}"
    
    await dialog_manager.switch_to(MainMenu.BALANCE_TRANSFER)


async def on_balance_transfer_recipient_history_back(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    """Возврат к вводу получателя из истории."""
    await dialog_manager.switch_to(MainMenu.BALANCE_TRANSFER_RECIPIENT)


async def on_balance_transfer_amount_click(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    """Открытие окна выбора суммы."""
    # Инициализируем pending_amount текущим значением amount при открытии
    transfer_data = dialog_manager.dialog_data.get("transfer_data", {})
    current_amount = transfer_data.get("amount")
    
    if current_amount:
        transfer_data["pending_amount"] = current_amount
    
    await dialog_manager.switch_to(MainMenu.BALANCE_TRANSFER_AMOUNT_VALUE)


async def on_balance_transfer_amount_preset_select(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    """Выбор preset суммы перевода."""
    # Извлекаем значение из widget_id
    widget_id = widget.widget_id
    amount_str = widget_id.replace("transfer_amount_", "")
    amount = int(amount_str)
    
    # Сохраняем сумму во временное поле pending_amount
    if "transfer_data" not in dialog_manager.dialog_data:
        dialog_manager.dialog_data["transfer_data"] = {}
    
    dialog_manager.dialog_data["transfer_data"]["pending_amount"] = amount


async def on_balance_transfer_amount_manual_input_click(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    """Открытие окна ручного ввода суммы."""
    await dialog_manager.switch_to(MainMenu.BALANCE_TRANSFER_AMOUNT_MANUAL)


@inject
async def on_balance_transfer_amount_manual_value_input(
    message: Message,
    widget: Any,
    dialog_manager: DialogManager,
    settings_service: FromDishka[SettingsService],
    i18n: FromDishka[TranslatorRunner],
) -> None:
    """Обработка ручного ввода суммы перевода."""
    dialog_manager.show_mode = ShowMode.EDIT
    
    # Валидируем сумму
    try:
        amount = int(message.text.strip())
    except (ValueError, AttributeError):
        error_msg = await message.answer(
            text=i18n.get("ntf-balance-invalid-amount"),
        )
        await asyncio.sleep(5)
        try:
            await error_msg.delete()
        except Exception:
            pass
        try:
            await message.delete()
        except Exception:
            pass
        return
    
    settings = await settings_service.get()
    transfer_settings = settings.features.transfers
    
    # Проверяем диапазон суммы
    min_amount = transfer_settings.min_amount if transfer_settings.min_amount else 0
    max_amount = transfer_settings.max_amount if transfer_settings.max_amount else 999999
    
    if amount < min_amount or amount > max_amount:
        error_msg = await message.answer(
            text=i18n.get("ntf-balance-transfer-amount-range", min=min_amount, max=max_amount),
        )
        await asyncio.sleep(5)
        try:
            await error_msg.delete()
        except Exception:
            pass
        try:
            await message.delete()
        except Exception:
            pass
        return
    
    # Сохраняем сумму во временное поле pending_amount
    if "transfer_data" not in dialog_manager.dialog_data:
        dialog_manager.dialog_data["transfer_data"] = {}
    
    dialog_manager.dialog_data["transfer_data"]["pending_amount"] = amount
    
    # Возвращаемся в окно выбора суммы
    await dialog_manager.switch_to(MainMenu.BALANCE_TRANSFER_AMOUNT_VALUE)
    
    try:
        await message.delete()
    except Exception:
        pass


async def on_balance_transfer_amount_cancel(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    """Отмена выбора суммы - очищаем pending и возврат в главное окно."""
    # Очищаем только pending_amount, сохраняем текущую назначенную сумму
    transfer_data = dialog_manager.dialog_data.get("transfer_data", {})
    transfer_data.pop("pending_amount", None)
    
    await dialog_manager.switch_to(MainMenu.BALANCE_TRANSFER)


async def on_balance_transfer_amount_manual_cancel(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    """Отмена ручного ввода суммы - возврат в окно выбора суммы."""
    await dialog_manager.switch_to(MainMenu.BALANCE_TRANSFER_AMOUNT_VALUE)


async def on_balance_transfer_amount_accept(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    """Принятие суммы - сохраняем pending в amount и возврат в главное окно."""
    transfer_data = dialog_manager.dialog_data.get("transfer_data", {})
    pending_amount = transfer_data.get("pending_amount")
    
    if pending_amount:
        # Переносим pending_amount в amount (текущая назначенная сумма)
        transfer_data["amount"] = pending_amount
        transfer_data.pop("pending_amount", None)
    
    await dialog_manager.switch_to(MainMenu.BALANCE_TRANSFER)


async def on_balance_transfer_message_click(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    """Открытие окна ввода сообщения."""
    await dialog_manager.switch_to(MainMenu.BALANCE_TRANSFER_MESSAGE)


async def on_balance_transfer_message_input(
    message: Message,
    widget: Any,
    dialog_manager: DialogManager,
) -> None:
    """Обработка ввода сообщения."""
    message_text = message.text.strip()
    
    # Проверяем длину сообщения (макс 200 символов)
    if len(message_text) > 200:
        message_text = message_text[:200]
    
    # Сохраняем сообщение в transfer_data
    transfer_data = dialog_manager.dialog_data.setdefault("transfer_data", {})
    transfer_data["message"] = message_text
    
    # Используем EDIT для замены сообщения, а не создания нового
    dialog_manager.show_mode = ShowMode.EDIT


async def on_balance_transfer_message_accept(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    """Принятие сообщения - возврат в главное меню."""
    await dialog_manager.switch_to(MainMenu.BALANCE_TRANSFER)


async def on_balance_transfer_message_cancel(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    """Отмена ввода сообщения - очищаем сообщение и возврат в главное меню."""
    transfer_data = dialog_manager.dialog_data.get("transfer_data", {})
    transfer_data.pop("message", None)
    
    await dialog_manager.switch_to(MainMenu.BALANCE_TRANSFER)


@inject
async def on_balance_transfer_send(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    user_service: FromDishka[UserService],
    settings_service: FromDishka[SettingsService],
    notification_service: FromDishka[NotificationService],
    balance_transfer_service: FromDishka[BalanceTransferService],
    referral_service: FromDishka[ReferralService],
    i18n: FromDishka[TranslatorRunner],
) -> None:
    """Отправка перевода - валидация и выполнение."""
    from src.services.balance_transfer import BalanceTransferService
    from src.core.enums import ReferralRewardType
    
    # Ответим на callback как можно раньше чтобы не истёк ID
    await callback.answer()
    
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    bot = callback.bot  # Используем bot из callback
    
    # Получаем данные перевода
    transfer_data = dialog_manager.dialog_data.get("transfer_data", {})
    recipient_id = transfer_data.get("recipient_id")
    recipient_name = transfer_data.get("recipient_name", "")
    amount = transfer_data.get("amount")
    
    # Проверяем что все данные заполнены
    if not recipient_id or not amount:
        error_msg = await callback.message.answer(
            text=i18n.get("ntf-balance-transfer-incomplete"),
        )
        await asyncio.sleep(5)
        try:
            await error_msg.delete()
        except Exception:
            pass
        return
    
    # Получаем настройки для расчета комиссии
    settings = await settings_service.get()
    transfer_settings = settings.features.transfers
    
    # Вычисляем комиссию
    if transfer_settings.commission_type == "percent":
        commission = int(amount * transfer_settings.commission_value / 100)
    else:
        commission = int(transfer_settings.commission_value)
    
    total = amount + commission
    
    # Проверяем режим баланса и получаем реферальный баланс
    is_balance_combined = await settings_service.is_balance_combined()
    referral_balance = await referral_service.get_pending_rewards_amount(
        telegram_id=user.telegram_id,
        reward_type=ReferralRewardType.MONEY,
    )
    
    # Вычисляем доступный баланс с учётом режима
    available_balance = user.balance + referral_balance if is_balance_combined else user.balance
    
    # Проверяем достаточно ли средств ПЕРЕД снятием
    if total > available_balance:
        error_msg = await callback.message.answer(
            text=i18n.get("ntf-balance-transfer-insufficient", required=total, balance=available_balance),
        )
        await asyncio.sleep(5)
        try:
            await error_msg.delete()
        except Exception:
            pass
        return
    
    # Получаем получателя ПЕРЕД снятием средств
    recipient = await user_service.get(recipient_id)
    if not recipient:
        error_msg = await callback.message.answer(
            text=i18n.get("ntf-balance-transfer-user-not-found"),
        )
        await asyncio.sleep(5)
        try:
            await error_msg.delete()
        except Exception:
            pass
        return
    
    # ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ - выполняем перевод
    try:
        # Списываем у отправителя с учетом режима баланса
        from_main, from_bonus = await user_service.subtract_from_combined_balance(
            user=user,
            amount=total,
            referral_balance=referral_balance,
            is_combined=is_balance_combined,
        )
        
        # Если списали с бонусного баланса, нужно вывести награды
        if from_bonus > 0:
            withdrawn = await referral_service.withdraw_pending_rewards(
                telegram_id=user.telegram_id,
                reward_type=ReferralRewardType.MONEY,
                amount=from_bonus,
            )
            logger.info(
                f"Withdrawn {withdrawn} from referral rewards for transfer "
                f"(user={user.telegram_id}, total={total})"
            )
        
        # Зачисляем получателю - в отдельном try-catch с откатом
        try:
            await user_service.add_to_balance(recipient, amount)
        except Exception as e:
            # Откатываем снятие денег со счета отправителя
            logger.error(f"Failed to add balance to recipient: {e}. Rolling back sender balance.")
            # Возвращаем деньги на основной баланс
            await user_service.add_to_balance(user, from_main)
            # Если были списаны бонусные деньги, их откат сложнее - просто логируем ошибку
            if from_bonus > 0:
                logger.error(
                    f"Cannot rollback bonus withdrawal of {from_bonus} for user {user.telegram_id}. "
                    f"Manual intervention may be required."
                )
            raise
        
        # Обновляем баланс в middleware_data
        user.balance -= from_main
        dialog_manager.middleware_data[USER_KEY] = user
        
        logger.info(
            f"Balance transfer: {user.telegram_id} -> {recipient.telegram_id}, "
            f"amount={amount}, commission={commission}, from_main={from_main}, from_bonus={from_bonus}"
        )
        
        # Сохраняем запись о переводе в историю
        try:
            await balance_transfer_service.create_transfer(
                sender_telegram_id=user.telegram_id,
                recipient_telegram_id=recipient.telegram_id,
                amount=amount,
                commission=commission,
                message=transfer_data.get("message"),
            )
        except Exception as e:
            logger.error(f"Failed to save transfer history: {e}")
        
        # Получаем сообщение если оно есть и экранируем HTML-символы
        message_text = transfer_data.get("message", "")
        has_message = 1 if message_text else 0
        # Экранируем HTML-специальные символы для безопасной передачи в Telegram
        escaped_message = html.escape(message_text) if message_text else ""
        
        # === ПЕРЕВОД УСПЕШЕН - далее только уведомления ===
        # Очищаем данные перевода сразу после успешного перевода
        dialog_manager.dialog_data.pop("transfer_data", None)
        
        # СНАЧАЛА обновляем меню получателя, чтобы он увидел новый баланс
        try:
            task = await redirect_to_main_menu_task.kiq(recipient.telegram_id)
            # Ждём выполнения задачи
            await task.wait_result(timeout=10)
            logger.debug(f"Recipient {recipient.telegram_id} menu updated, balance refreshed")
        except Exception as refresh_error:
            logger.error(f"Failed to refresh recipient menu: {refresh_error}")
        
        # ЗАТЕМ запускаем ОТЛОЖЕННУЮ задачу для отправки уведомления
        # Задача выполнится через 8 секунд - это гарантирует что меню уже отобразилось
        try:
            notification_text = i18n.get(
                "ntf-balance-transfer-received",
                amount=amount,
                sender=user.name or str(user.telegram_id),
                has_message=has_message,
                message=escaped_message,
            )
            
            # Запускаем отложенную задачу (НЕ ждём результата - fire and forget)
            await send_delayed_transfer_notification_task.kiq(
                recipient_telegram_id=recipient.telegram_id,
                notification_text=notification_text,
                delay_seconds=8,
            )
            logger.debug(f"Scheduled delayed notification for {recipient.telegram_id} (+8 sec)")
        except Exception as e:
            logger.error(f"Failed to schedule transfer notification for {recipient.telegram_id}: {e}")
        
        # Отправляем системное уведомление разработчику (не влияет на результат перевода)
        try:
            # Вычисляем итоговый баланс отправителя с учетом режима
            sender_balance_after = user.balance
            if is_balance_combined:
                # Обновляем реферальный баланс после вывода
                referral_balance_after = await referral_service.get_pending_rewards_amount(
                    telegram_id=user.telegram_id,
                    reward_type=ReferralRewardType.MONEY,
                )
                sender_balance_after += referral_balance_after
            
            # Вычисляем итоговый баланс получателя с учетом режима
            recipient_balance_after = recipient.balance
            if is_balance_combined:
                recipient_referral_balance = await referral_service.get_pending_rewards_amount(
                    telegram_id=recipient.telegram_id,
                    reward_type=ReferralRewardType.MONEY,
                )
                recipient_balance_after += recipient_referral_balance
            
            await notification_service.system_notify(
                ntf_type=SystemNotificationType.BALANCE_TRANSFER,
                payload=MessagePayload.not_deleted(
                    i18n_key="ntf-event-balance-transfer",
                    i18n_kwargs={
                        "sender_id": str(user.telegram_id),
                        "sender_name": user.name or str(user.telegram_id),
                        "sender_balance": sender_balance_after,
                        "recipient_id": str(recipient.telegram_id),
                        "recipient_name": recipient.name or str(recipient.telegram_id),
                        "recipient_balance": recipient_balance_after,
                        "amount": amount,
                        "commission": commission,
                        "total": total,
                        "has_message": has_message,
                        "message": escaped_message,
                    },
                ),
            )
        except Exception as e:
            logger.error(f"Failed to send system notification about transfer: {e}")
        
        # Возвращаемся в меню баланса ПЕРЕД отправкой уведомления
        await dialog_manager.switch_to(MainMenu.BALANCE)
        
        # Показываем уведомление об успехе с кнопкой "Готово" (не влияет на результат перевода)
        try:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="✅ Готово", callback_data="close_success_transfer", style="success")]
                ]
            )
            
            success_msg = await callback.message.answer(
                text=i18n.get(
                    "ntf-balance-transfer-success", 
                    amount=amount, 
                    recipient=recipient_name, 
                    commission=commission,
                    has_message=has_message,
                    message=escaped_message,
                ),
                reply_markup=keyboard,
            )
        except Exception as e:
            logger.error(f"Failed to send success notification to sender: {e}")
        
    except Exception as e:
        logger.error(f"{log(user)} Failed to transfer balance: {e}")
        error_msg = await callback.message.answer(
            text=i18n.get("ntf-balance-transfer-error"),
        )
        await asyncio.sleep(5)
        try:
            await error_msg.delete()
        except Exception:
            pass


async def on_balance_transfer_cancel(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    """Отмена перевода - возврат в меню баланса."""
    # Очищаем данные перевода
    dialog_manager.dialog_data.pop("transfer_data", None)
    
    await dialog_manager.switch_to(MainMenu.BALANCE)


@inject
async def on_extra_devices_list(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    """Переход к списку купленных дополнительных устройств."""
    from src.bot.states import Subscription
    await dialog_manager.start(Subscription.EXTRA_DEVICES_LIST, mode=StartMode.RESET_STACK)


@inject
async def on_add_device(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    """Переход к добавлению дополнительных устройств."""
    from src.bot.states import Subscription
    await dialog_manager.start(Subscription.ADD_DEVICE_SELECT_COUNT, mode=StartMode.RESET_STACK)


@inject
async def on_delete_extra_device_purchase(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    extra_device_service: FromDishka[ExtraDeviceService],
    subscription_service: FromDishka[SubscriptionService],
    remnawave_service: FromDishka[RemnawaveService],
    user_service: FromDishka[UserService],
    notification_service: FromDishka[NotificationService],
) -> None:
    """Удалить покупку дополнительных устройств из меню устройств."""
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    
    # Получаем purchase_id из SubManager (ListGroup)
    if isinstance(dialog_manager, SubManager):
        purchase_id = int(dialog_manager.item_id)
    else:
        return
    
    if not purchase_id:
        return
    
    # Получаем информацию о покупке
    purchase = await extra_device_service.get(purchase_id)
    if not purchase:
        return
    
    subscription = user.current_subscription
    if not subscription:
        return
    
    # Удаляем покупку и уменьшаем лимит устройств
    device_count_to_remove = purchase.device_count
    await extra_device_service.delete(purchase_id)
    
    # Обновляем лимит устройств в подписке
    new_extra_devices = max(0, (subscription.extra_devices or 0) - device_count_to_remove)
    base_device_limit = (subscription.plan.device_limit if subscription.plan and subscription.plan.device_limit else 0)
    current_device_limit = subscription.device_limit if subscription.device_limit else 0
    new_device_limit = max(base_device_limit, current_device_limit - device_count_to_remove)
    
    subscription.extra_devices = new_extra_devices
    subscription.device_limit = new_device_limit
    
    await subscription_service.update(subscription)
    
    # Обновляем в Remnawave
    await remnawave_service.updated_user(
        user=user,
        uuid=subscription.user_remna_id,
        subscription=subscription,
    )
    
    # Очищаем кеш
    await user_service.clear_user_cache(user.telegram_id)
    
    logger.info(f"{log(user)} Deleted extra device purchase '{purchase_id}', removed {device_count_to_remove} devices")
    
    await notification_service.notify_user(
        user=user,
        payload=MessagePayload(i18n_key="ntf-extra-device-deleted"),
    )
    
    await callback.answer()