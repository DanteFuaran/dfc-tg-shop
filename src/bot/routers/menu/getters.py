from typing import Any
import html

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner
from loguru import logger

from src.core.config import AppConfig
from src.core.enums import BalanceMode, Currency, ReferralRewardType
from src.core.exceptions import MenuRenderingError
from src.core.utils.formatters import (
    format_price,
    format_username_to_url,
    i18n_format_device_limit,
    i18n_format_expire_time,
    i18n_format_traffic_limit,
)
from src.core.utils.balance import format_balance, get_display_balance
from src.core.utils.discount import calculate_user_discount
from src.infrastructure.database.models.dto import UserDto
from src.services.balance_transfer import BalanceTransferService
from src.services.payment_gateway import PaymentGatewayService
from src.services.plan import PlanService
from src.services.referral import ReferralService
from src.services.remnawave import RemnawaveService
from src.services.settings import SettingsService
from src.services.subscription import SubscriptionService
from src.services.extra_device import ExtraDeviceService


@inject
async def menu_getter(
    dialog_manager: DialogManager,
    config: AppConfig,
    user: UserDto,
    i18n: FromDishka[TranslatorRunner],
    plan_service: FromDishka[PlanService],
    subscription_service: FromDishka[SubscriptionService],
    settings_service: FromDishka[SettingsService],
    referral_service: FromDishka[ReferralService],
    extra_device_service: FromDishka[ExtraDeviceService],
    **kwargs: Any,
) -> dict[str, Any]:
    try:
        settings = await settings_service.get()
        referral = await referral_service.get_referral_by_referred(user.telegram_id)
        has_used_trial = await subscription_service.has_used_trial(user.telegram_id)
        ref_link = await referral_service.get_ref_link(user.referral_code)
        referral_balance = await referral_service.get_pending_rewards_amount(
            user.telegram_id,
            ReferralRewardType.MONEY,
        )

        is_invited = bool(referral)

        # Используем новый метод, который учитывает приглашение пользователя
        plan = await plan_service.get_appropriate_trial_plan(user, is_invited=is_invited)
        support_username = config.bot.support_username.get_secret_value()
        support_link = format_username_to_url(support_username, i18n.get("contact-support-help"))
        
        # Invite message from settings (один объект settings — без лишних запросов)
        try:
            invite_message = str(settings.referral.invite_message) if settings.referral.invite_message else None
        except Exception:
            invite_message = None
        
        if invite_message:
            invite_message = invite_message.format(url=ref_link, name="VPN", space="\n") if "{url}" in invite_message else invite_message.replace("$url", ref_link).replace("$name", "VPN")
            if invite_message.startswith("\n"):
                invite_message = invite_message[1:]
        else:
            invite_message = f"\nJoin us! {ref_link}"

        # Вычисляем данные о скидке пользователя
        discount_info = calculate_user_discount(user)

        # Извлекаем все нужные поля из единственного объекта settings
        is_balance_combined = settings.features.balance_mode == BalanceMode.COMBINED
        default_currency = settings.default_currency
        is_referral_enabled = settings.referral.enable
        is_promocodes_enabled = settings.features.promocodes_enabled
        community_url = settings.features.community_url or ""
        is_community_enabled = settings.features.community_enabled and bool(community_url)
        is_tos_enabled = settings.features.tos_enabled
        tos_url = settings.rules_link.get_secret_value() or "https://telegra.ph/"
        is_balance_enabled = settings.features.balance_enabled
        currency_rates = settings.features.currency_rates

        display_balance = get_display_balance(user.balance, referral_balance, is_balance_combined)
        formatted_balance = format_balance(display_balance, default_currency, currency_rates)
        
        # Проверяем наличие дополнительных устройств для показа кнопки "Мои устройства"
        has_extra_devices_purchases = False
        subscription = user.current_subscription

        # Если подписка не загружена в DTO (например, bg_manager.start без middleware),
        # перезапрашиваем из БД
        if not subscription:
            subscription = await subscription_service.get_current(telegram_id=user.telegram_id)

        if subscription:
            purchases = await extra_device_service.get_by_subscription(subscription.id)
            has_extra_devices_purchases = len(purchases) > 0

        base_data = {
            "user_id": str(user.telegram_id),
            "user_name": user.name,
            "discount_value": discount_info.value,
            "discount_is_temporary": 1 if discount_info.is_temporary else 0,
            "discount_is_permanent": 1 if discount_info.is_permanent else 0,
            "discount_remaining": discount_info.remaining_days,
            "balance": formatted_balance,
            "referral_balance": format_balance(referral_balance, default_currency, currency_rates),
            "referral_code": user.referral_code,
            "support": support_link,
            "invite": invite_message,
            "has_subscription": bool(subscription),
            "is_app": config.bot.is_mini_app,
            "is_referral_enable": 1 if is_referral_enabled else 0,
            "is_promocodes_enabled": is_promocodes_enabled,
            # Настройки функционала
            "community_url": community_url,
            "is_community_enabled": is_community_enabled,
            "is_tos_enabled": is_tos_enabled,
            "tos_url": tos_url,
            "is_balance_enabled": 1 if is_balance_enabled else 0,
            "is_balance_separate": 1 if not is_balance_combined else 0,
            # Показывать кнопку "Мои устройства" всегда
            "show_devices_button": True,
        }

        if not subscription:
            base_data.update(
                {
                    "status": None,
                    "is_trial": False,
                    "trial_available": not has_used_trial and plan,
                    "has_device_limit": False,
                    "connectable": False,
                    "device_limit_bonus": 0,
                }
            )
            return base_data

        extra_devices = subscription.extra_devices or 0
        
        # Вычисляем бонус устройств (разница между реальным лимитом из Remnawave и планом, БЕЗ купленных доп.)
        plan_device_limit = subscription.plan.device_limit if subscription.plan.device_limit > 0 else 0
        actual_device_limit = subscription.device_limit
        device_limit_bonus = max(0, actual_device_limit - plan_device_limit - extra_devices) if plan_device_limit > 0 else 0
        
        base_data.update(
            {
                "status": subscription.get_status,
                "type": subscription.get_subscription_type,
                "plan_name": subscription.plan.name,
                "current_plan_name": subscription.plan.name,
                "traffic_limit": i18n_format_traffic_limit(subscription.traffic_limit),
                "device_limit": i18n_format_device_limit(plan_device_limit if plan_device_limit > 0 else subscription.device_limit),
                "device_limit_number": plan_device_limit if plan_device_limit > 0 else subscription.device_limit,
                "device_limit_bonus": device_limit_bonus,
                "extra_devices": extra_devices,
                "expire_time": i18n_format_expire_time(subscription.expire_at),
                "is_trial": subscription.is_trial,
                "traffic_strategy": subscription.traffic_limit_strategy,
                "reset_time": subscription.get_expire_time,
                "has_device_limit": subscription.has_devices_limit
                if subscription.is_active
                else False,
                "connectable": subscription.is_active,
                "url": config.bot.mini_app_url or subscription.url,
            }
        )

        return base_data
    except Exception as exception:
        raise MenuRenderingError(str(exception)) from exception


# Ссылки для скачивания приложений по платформам
DOWNLOAD_URLS = {
    "android": "https://play.google.com/store/apps/details?id=com.happproxy",
    "windows": "https://github.com/Happ-proxy/happ-desktop/releases/latest/download/setup-Happ.x64.exe",
    "iphone": "https://apps.apple.com/app/happ-proxy-utility-plus/id6746188973",
    "macos": "https://github.com/Happ-proxy/happ-desktop/releases/",
}

PLATFORM_NAMES = {
    "android": "📱 Android",
    "windows": "🖥 Windows",
    "iphone": "🍏 iPhone",
    "macos": "💻 macOS",
}


@inject
async def connect_getter(
    dialog_manager: DialogManager,
    config: AppConfig,
    user: UserDto,
    **kwargs: Any,
) -> dict[str, Any]:
    """Геттер для окна подключения с инструкцией."""
    
    subscription = user.current_subscription
    subscription_url = subscription.url if subscription else ""
    subscription_key = subscription.url.split("/")[-1] if subscription and subscription.url else ""
    
    # URL для скачивания с автоопределением ОС
    domain = config.domain.get_secret_value()
    download_url = f"https://{domain}/api/v1/download"
    
    # URL для добавления в приложение Happ через редирект
    happ_add_url = f"https://{domain}/api/v1/connect/{subscription_url}" if subscription_url else ""
    
    return {
        "url": config.bot.mini_app_url or subscription_url,
        "download_url": download_url,
        "subscription_url": subscription_url,
        "subscription_key": subscription_key,
        "happ_add_url": happ_add_url,
        "is_app": config.bot.is_mini_app,
        "has_subscription": 1 if subscription else 0,
    }


@inject
async def devices_getter(
    dialog_manager: DialogManager,
    user: UserDto,
    i18n: FromDishka[TranslatorRunner],
    remnawave_service: FromDishka[RemnawaveService],
    settings_service: FromDishka[SettingsService],
    referral_service: FromDishka[ReferralService],
    extra_device_service: FromDishka[ExtraDeviceService],
    **kwargs: Any,
) -> dict[str, Any]:
    from src.core.enums import ReferralRewardType
    
    subscription = user.current_subscription
    
    settings = await settings_service.get()
    referral_balance = await referral_service.get_pending_rewards_amount(
        telegram_id=user.telegram_id,
        reward_type=ReferralRewardType.MONEY,
    )

    # Извлекаем флаги из единственного объекта settings
    is_balance_enabled = settings.features.balance_enabled
    is_balance_combined = settings.features.balance_mode == BalanceMode.COMBINED
    is_balance_separate = not is_balance_combined
    is_referral_enabled = settings.referral.enable
    default_currency = settings.default_currency
    currency_rates = settings.features.currency_rates
    
    display_balance = get_display_balance(user.balance, referral_balance, is_balance_combined)

    # Вычисляем данные о скидке пользователя
    discount_info = calculate_user_discount(user)
    
    # Проверяем включён ли функционал доп. устройств
    is_extra_devices_enabled = settings.features.extra_devices.enabled
    
    # Если нет подписки - показываем пустой список устройств
    if not subscription:
        return {
            "current_count": 0,
            "max_count": "0",
            "devices": [],
            "devices_empty": True,
            # Данные подписки
            "plan_name": "—",
            "current_plan_name": "—",
            "traffic_limit": "—",
            "device_limit_number": 0,
            "device_limit_bonus": 0,
            "extra_devices": 0,
            "expire_time": "—",
            # Список покупок доп. устройств
            "extra_device_purchases": [],
            "has_extra_device_purchases": 0,
            # Флаги для кнопок
            "can_add_device": False,
            "can_add_extra_device": 1 if is_extra_devices_enabled else 0,
            "has_subscription": False,
            "is_balance_enabled": 1 if is_balance_enabled else 0,
            "is_balance_separate": 1 if is_balance_separate else 0,
            "is_referral_enable": 1 if is_referral_enabled else 0,
            # Слоты устройств (пустые без подписки)
            "device_slots": [],
            "has_device_slots": 0,
            # Данные профиля для frg-user
            "user_id": str(user.telegram_id),
            "user_name": user.name,
            "discount_value": discount_info.value,
            "discount_is_temporary": 1 if discount_info.is_temporary else 0,
            "discount_is_permanent": 1 if discount_info.is_permanent else 0,
            "discount_remaining": discount_info.remaining_days,
"balance": format_balance(display_balance, default_currency, currency_rates),
            "referral_balance": format_balance(referral_balance, default_currency, currency_rates),
            "referral_code": user.referral_code,
        }

    devices = await remnawave_service.get_devices_user(user)

    formatted_devices = [
        {
            "short_hwid": device.hwid[:32],
            "hwid": device.hwid,
            "platform": device.platform,
            "device_model": device.device_model,
            "user_agent": device.user_agent,
        }
        for device in devices
    ]
    
    # Сортируем устройства по hwid для стабильного порядка
    # Это предотвращает сдвиг списка при добавлении новых устройств
    formatted_devices.sort(key=lambda d: d["hwid"])

    dialog_manager.dialog_data["hwid_map"] = formatted_devices
    
    # Добавляем данные подписки для отображения в frg-subscription-devices
    extra_devices = subscription.extra_devices or 0
    plan_device_limit = subscription.plan.device_limit if subscription.plan and subscription.plan.device_limit > 0 else 0
    actual_device_limit = subscription.device_limit
    device_limit_bonus = max(0, actual_device_limit - plan_device_limit - extra_devices) if plan_device_limit > 0 else 0
    
    # Проверяем включён ли функционал доп. устройств (из уже загруженных settings)
    is_extra_devices_enabled = settings.features.extra_devices.enabled
    
    # Определяем показывать ли кнопку "Управление доп. устройствами"
    # Условия: функционал включён И (есть extra_devices > 0 ИЛИ (подписка не триал и не реферальная))
    # ИЛИ есть история покупок доп. устройств (даже если подписка истекла)
    plan_name_lower = subscription.plan.name.lower() if subscription.plan else ""
    is_trial_subscription = subscription.is_trial or "пробн" in plan_name_lower
    is_referral_subscription = "реферал" in plan_name_lower
    is_import_subscription = "import" in (subscription.plan.name.lower() if subscription.plan else "") or (subscription.tag and "import" in subscription.tag.lower())
    
    # Получаем активные покупки доп. устройств
    purchases = []
    try:
        purchases = await extra_device_service.get_active_by_subscription(subscription.id)
    except Exception:
        pass
    
    # Создаём объединённый список слотов устройств
    # Порядок: базовые (из плана) → бонусные (из админки) → купленные (extra)
    device_slots = []
    slot_hwid_map = {}  # Маппинг slot_index -> hwid для удаления устройств
    slot_purchase_map = {}  # Маппинг slot_index -> purchase_id для удаления пустых extra слотов
    devices_copy = list(formatted_devices)  # Копия для распределения
    slot_index = 0
    
    # 1. Базовые слоты подписки (из плана, срок = срок подписки)
    for i in range(plan_device_limit):
        # Пытаемся занять слот устройством
        if devices_copy:
            device = devices_copy.pop(0)
            slot = {
                "id": str(slot_index),  # Короткий индекс для callback_data
                "slot_type": "base",
                "days_display": "∞",
                "is_occupied": True,
                "show_delete_button": False,
                "show_trash_button": True,
                "show_extra_trash_button": False,
                "show_pending_text": False,
                "device_info": f"{device['platform']} - {device['device_model']}",
            }
            slot_hwid_map[str(slot_index)] = device["short_hwid"]
        else:
            slot = {
                "id": str(slot_index),
                "slot_type": "base",
                "days_display": "∞",
                "is_occupied": False,
                "show_delete_button": False,
                "show_trash_button": False,
                "show_extra_trash_button": False,
                "show_pending_text": False,
                "device_info": i18n.get("frg-empty-slot"),
            }
        device_slots.append(slot)
        slot_index += 1
    
    # 2. Бонусные слоты (добавленные через админ-панель, срок = срок подписки)
    for i in range(device_limit_bonus):
        # Пытаемся занять слот устройством
        if devices_copy:
            device = devices_copy.pop(0)
            slot = {
                "id": str(slot_index),
                "slot_type": "bonus",
                "days_display": "∞",
                "is_occupied": True,
                "show_delete_button": False,
                "show_trash_button": True,
                "show_extra_trash_button": False,
                "show_pending_text": False,
                "device_info": f"{device['platform']} - {device['device_model']}",
            }
            slot_hwid_map[str(slot_index)] = device["short_hwid"]
        else:
            slot = {
                "id": str(slot_index),
                "slot_type": "bonus",
                "days_display": "∞",
                "is_occupied": False,
                "show_delete_button": False,
                "show_trash_button": False,
                "show_extra_trash_button": False,
                "show_pending_text": False,
                "device_info": i18n.get("frg-empty-slot"),
            }
        device_slots.append(slot)
        slot_index += 1
    
    # 3. Слоты из покупок (с ограниченным сроком)
    for p in purchases:
        # Логируем информацию о покупке для отладки
        logger.debug(
            f"Extra device purchase: id={p.id}, expires_at={p.expires_at}, "
            f"days_remaining={p.days_remaining}, device_count={p.device_count}, pending_deletion={p.pending_deletion}"
        )
        for j in range(p.device_count):
            # Пытаемся занять слот устройством
            days_word = i18n.get("frg-day-plural", value=p.days_remaining)
            if devices_copy:
                device = devices_copy.pop(0)
                slot = {
                    "id": str(slot_index),  # Короткий индекс для callback_data
                    "purchase_id": str(p.id),
                    "slot_type": "extra",
                    "days_display": f"{p.days_remaining} {days_word}",
                    "is_occupied": True,
                    "pending_deletion": p.pending_deletion,
                    # ❌ - помечает слот на удаление (для extra слотов с устройством)
                    "show_delete_button": not p.pending_deletion,
                    # 🗑 - удаляет устройство из слота (очищает слот)
                    "show_trash_button": not p.pending_deletion,
                    "show_extra_trash_button": False,  # Не используем
                    "show_pending_text": p.pending_deletion,  # Показываем "На удалении" если pending
                    "device_info": f"{device['platform']} - {device['device_model']}",
                }
                slot_hwid_map[str(slot_index)] = device["short_hwid"]
                # Сохраняем purchase_id для всех extra слотов (и занятых тоже)
                slot_purchase_map[str(slot_index)] = p.id
            else:
                slot = {
                    "id": str(slot_index),
                    "purchase_id": str(p.id),
                    "slot_type": "extra",
                    "days_display": f"{p.days_remaining} {days_word}",
                    "is_occupied": False,
                    "pending_deletion": p.pending_deletion,
                    # ❌ - помечает слот на удаление (для пустых extra слотов)
                    "show_delete_button": not p.pending_deletion,
                    "show_trash_button": False,  # Нет устройства - нечего очищать
                    "show_extra_trash_button": False,
                    "show_pending_text": p.pending_deletion,
                    "device_info": i18n.get("frg-empty-slot"),
                }
                # Сохраняем purchase_id для удаления пустого слота
                slot_purchase_map[str(slot_index)] = p.id
            device_slots.append(slot)
            slot_index += 1
    
    # Сохраняем данные для обработчиков
    dialog_manager.dialog_data["slot_hwid_map"] = slot_hwid_map
    dialog_manager.dialog_data["slot_purchase_map"] = slot_purchase_map
    dialog_manager.dialog_data["extra_device_purchases"] = [
        {"id": p.id, "device_count": p.device_count}
        for p in purchases
    ]
    
    has_extra_device_purchases = len(purchases) > 0
    
    # Показываем кнопку добавления устройств если:
    # Функционал включён И подписка активна И это не триал/реферальная/импорт подписка
    can_add_extra_device = (
        is_extra_devices_enabled 
        and subscription.is_active 
        and not is_trial_subscription 
        and not is_referral_subscription
        and not is_import_subscription
    )
    
    # Оптимизированная фильтрация слотов:
    # - Всегда показываем все extra слоты (куплены и имеют срок действия)
    # - Для базовых и бонусных слотов применяем правило:
    #   - Если <= 10, показываем все
    #   - Если > 10, показываем первые 10, потом дополнительно показываем по 1,
    #     если из видимых >= 8 занято
    
    extra_slots = [slot for slot in device_slots if slot["slot_type"] == "extra"]
    base_bonus_slots = [slot for slot in device_slots if slot["slot_type"] in ["base", "bonus"]]
    
    if len(base_bonus_slots) <= 10:
        # Если базовых и бонусных слотов 10 или меньше, показываем все
        filtered_slots = base_bonus_slots + extra_slots
    else:
        # Если больше 10, применяем правило прогрессивного раскрытия
        visible_count = 10
        
        # Считаем, сколько занято в видимых слотах
        while visible_count < len(base_bonus_slots):
            visible_slots = base_bonus_slots[:visible_count]
            occupied_count = sum(1 for slot in visible_slots if slot["is_occupied"])
            
            # Если 8 или больше занято из видимых, показываем еще 1
            if occupied_count >= 8:
                visible_count += 1
            else:
                break
        
        filtered_slots = base_bonus_slots[:visible_count] + extra_slots
    
    device_slots = filtered_slots

    return {
        "current_count": len(devices),
        "max_count": i18n_format_device_limit(subscription.device_limit),
        "devices": formatted_devices,
        "devices_empty": len(device_slots) == 0,
        # Слоты устройств (базовые + купленные)
        "device_slots": device_slots,
        "has_device_slots": 1 if device_slots else 0,
        # Данные подписки
        "plan_name": subscription.plan.name if subscription.plan else "Unknown",
        "current_plan_name": subscription.plan.name if subscription.plan else "Unknown",
        "traffic_limit": i18n_format_traffic_limit(subscription.traffic_limit),
        "device_limit_number": plan_device_limit if plan_device_limit > 0 else subscription.device_limit,
        "device_limit_bonus": device_limit_bonus,
        "extra_devices": extra_devices,
        "expire_time": i18n_format_expire_time(subscription.expire_at),
        # Флаги для покупок
        "has_extra_device_purchases": 1 if has_extra_device_purchases else 0,
        # Флаги для кнопок
        "can_add_device": subscription.is_active and subscription.has_devices_limit,
        "can_add_extra_device": 1 if can_add_extra_device else 0,
        "has_subscription": True,
        "is_balance_enabled": 1 if is_balance_enabled else 0,
        "is_balance_separate": 1 if is_balance_separate else 0,
        "is_referral_enable": 1 if is_referral_enabled else 0,
        # Данные профиля для frg-user
        "user_id": str(user.telegram_id),
        "user_name": user.name,
        "discount_value": discount_info.value,
        "discount_is_temporary": 1 if discount_info.is_temporary else 0,
        "discount_is_permanent": 1 if discount_info.is_permanent else 0,
        "discount_remaining": discount_info.remaining_days,
        "balance": format_balance(display_balance, default_currency, currency_rates),
        "referral_balance": format_balance(referral_balance, default_currency, currency_rates),
        "referral_code": user.referral_code,
    }


@inject
async def invite_getter(
    dialog_manager: DialogManager,
    user: UserDto,
    config: AppConfig,
    i18n: FromDishka[TranslatorRunner],
    settings_service: FromDishka[SettingsService],
    referral_service: FromDishka[ReferralService],
    **kwargs: Any,
) -> dict[str, Any]:
    from datetime import datetime, timezone
    from src.core.enums import ReferralRewardType
    
    full_settings = await settings_service.get()
    referrals = await referral_service.get_referral_count(user.telegram_id)
    payments = await referral_service.get_reward_count(user.telegram_id)
    ref_link = await referral_service.get_ref_link(user.referral_code)
    referral_balance = await referral_service.get_pending_rewards_amount(user.telegram_id, ReferralRewardType.MONEY)
    total_bonus = await referral_service.get_total_rewards_amount(user.telegram_id, ReferralRewardType.MONEY)

    # Извлекаем флаги из settings (без дополнительных запросов)
    is_balance_combined = full_settings.features.balance_mode == BalanceMode.COMBINED
    is_balance_separate = not is_balance_combined
    is_balance_enabled = full_settings.features.balance_enabled
    is_referral_enabled = full_settings.referral.enable

    support_username = config.bot.support_username.get_secret_value()
    support_link = format_username_to_url(
        support_username, i18n.get("contact-support-withdraw-points")
    )
    
    # Get invite message from settings
    # Replace placeholders with actual values
    try:
        invite_message = str(full_settings.referral.invite_message) if full_settings.referral.invite_message else None
    except Exception:
        invite_message = None
    
    if invite_message:
        # Support both Python format {url}/{name} and legacy $url/$name
        # Also support {space} for newline
        invite_message = invite_message.format(url=ref_link, name="VPN", space="\n") if "{url}" in invite_message else invite_message.replace("$url", ref_link).replace("$name", "VPN")
    else:
        invite_message = f"\n{i18n.get('msg-invite-welcome')}\n\n=> [{i18n.get('msg-invite-connect')}]({ref_link})"
    
    # Вычисляем данные о скидке пользователя
    discount_info = calculate_user_discount(user)
    
    # Prepare subscription data
    subscription = user.current_subscription
    subscription_data = {}
    
    logger.debug(f"🔍 [invite_getter] user={user.telegram_id}: subscription={subscription}, is_active={subscription.is_active if subscription else 'None'}")
    
    if subscription:
        extra_devices = subscription.extra_devices or 0
        # Вычисляем бонус устройств (БЕЗ купленных доп.)
        plan_device_limit = subscription.plan.device_limit if subscription.plan.device_limit > 0 else 0
        actual_device_limit = subscription.device_limit
        device_limit_bonus = max(0, actual_device_limit - plan_device_limit - extra_devices) if plan_device_limit > 0 else 0
        
        subscription_data = {
            "status": subscription.get_status,
            "plan_name": subscription.plan.name,
            "current_plan_name": subscription.plan.name,
            "traffic_limit": i18n_format_traffic_limit(subscription.traffic_limit),
            "device_limit": i18n_format_device_limit(plan_device_limit if plan_device_limit > 0 else subscription.device_limit),
            "device_limit_number": plan_device_limit if plan_device_limit > 0 else subscription.device_limit,
            "device_limit_bonus": device_limit_bonus,
            "extra_devices": extra_devices,
            "expire_time": i18n_format_expire_time(subscription.expire_at),
            "is_trial": subscription.is_trial,
            "traffic_strategy": subscription.traffic_limit_strategy,
            "reset_time": subscription.get_expire_time,
        }
    else:
        subscription_data = {
            "status": None,
            "is_trial": False,
            "device_limit_bonus": 0,
        }
    
    # Prepare referral reward display for info text
    max_level = full_settings.referral.level.value
    reward_config = full_settings.referral.reward.config
    
    # Format rewards based on level
    from src.core.enums import ReferralLevel
    reward_level_1_value = reward_config.get(ReferralLevel.FIRST, 0)
    reward_level_2_value = reward_config.get(ReferralLevel.SECOND, 0)
    
    default_currency = full_settings.default_currency
    currency_rates = full_settings.features.currency_rates
    
    return {
        "user_id": str(user.telegram_id),
        "user_name": user.name,
        "referral_code": user.referral_code,
        "balance": format_balance(get_display_balance(user.balance, referral_balance, is_balance_combined), default_currency, currency_rates),
        "referral_balance": format_balance(referral_balance, default_currency, currency_rates) if is_balance_separate else format_balance(0, default_currency, currency_rates),  # Скрываем в режиме COMBINED
        "discount_value": discount_info.value,
        "discount_is_temporary": 1 if discount_info.is_temporary else 0,
        "discount_is_permanent": 1 if discount_info.is_permanent else 0,
        "discount_remaining": discount_info.remaining_days,
        "total_bonus": format_balance(total_bonus, default_currency, currency_rates),
        "reward_type": full_settings.referral.reward.type,
        "referrals": referrals,
        "payments": payments,
        "is_points_reward": full_settings.referral.reward.is_money,
        "has_balance": (referral_balance > 0) and is_balance_separate,  # Показываем только в режиме SEPARATE
        "is_balance_enabled": 1 if is_balance_enabled else 0,
        "is_balance_separate": 1 if is_balance_separate else 0,  # Флаг раздельного режима баланса
        "is_referral_enable": 1 if is_referral_enabled else 0,
        "referral_link": ref_link,
        "invite": invite_message,
        "withdraw": support_link,
        "ref_max_level": max_level,
        "ref_reward_level_1_value": reward_level_1_value,
        "ref_reward_level_2_value": reward_level_2_value,
        "ref_reward_strategy": full_settings.referral.reward.strategy,
        "ref_reward_type": full_settings.referral.reward.type,
        "currency_symbol": default_currency.symbol,
        **subscription_data,
    }


@inject
async def invite_about_getter(
    dialog_manager: DialogManager,
    i18n: FromDishka[TranslatorRunner],
    settings_service: FromDishka[SettingsService],
    **kwargs: Any,
) -> dict[str, Any]:
    settings = await settings_service.get_referral_settings()
    reward_config = settings.reward.config

    max_level = settings.level.value
    identical_reward = settings.reward.is_identical

    reward_levels: dict[str, str] = {}
    for lvl, val in reward_config.items():
        if lvl.value <= max_level:
            reward_levels[f"reward_level_{lvl.value}"] = i18n.get(
                "msg-invite-reward",
                value=val,
                reward_strategy_type=settings.reward.strategy,
                reward_type=settings.reward.type,
            )

    return {
        **reward_levels,
        "reward_type": settings.reward.type,
        "reward_strategy_type": settings.reward.strategy,
        "accrual_strategy": settings.accrual_strategy,
        "identical_reward": identical_reward,
        "max_level": max_level,
    }


async def invite_edit_code_getter(
    dialog_manager: DialogManager,
    user: UserDto,
    **kwargs: Any,
) -> dict[str, Any]:
    """Геттер для окна смены реферального кода."""
    return {
        "referral_code": user.referral_code,
        "ref_code_error": dialog_manager.dialog_data.get("ref_code_error", ""),
    }


@inject
async def balance_menu_getter(
    dialog_manager: DialogManager,
    user: UserDto,
    plan_service: FromDishka[PlanService],
    subscription_service: FromDishka[SubscriptionService],
    referral_service: FromDishka[ReferralService],
    settings_service: FromDishka[SettingsService],
    **kwargs: Any,
) -> dict[str, Any]:
    from datetime import datetime, timezone
    from src.core.enums import ReferralRewardType
    
    full_settings = await settings_service.get()
    referral = await referral_service.get_referral_by_referred(user.telegram_id)
    has_used_trial = await subscription_service.has_used_trial(user.telegram_id)
    referral_balance = await referral_service.get_pending_rewards_amount(user.telegram_id, ReferralRewardType.MONEY)

    is_invited = bool(referral)
    plan = await plan_service.get_appropriate_trial_plan(user, is_invited=is_invited)

    # Вычисляем данные о скидке пользователя
    discount_info = calculate_user_discount(user)

    # Извлекаем все флаги из единственного объекта settings
    is_balance_enabled = full_settings.features.balance_enabled
    is_balance_combined = full_settings.features.balance_mode == BalanceMode.COMBINED
    is_balance_separate = not is_balance_combined
    is_transfers_enabled = full_settings.features.transfers.enabled
    is_referral_enabled = full_settings.referral.enable
    default_currency = full_settings.default_currency
    currency_rates = full_settings.features.currency_rates
    
    # В режиме COMBINED показываем сумму основного и бонусного баланса
    display_balance = get_display_balance(user.balance, referral_balance, is_balance_combined)
    formatted_balance = format_balance(display_balance, default_currency, currency_rates)
    formatted_referral_balance = format_balance(referral_balance, default_currency, currency_rates)
    
    base_data = {
        "user_id": str(user.telegram_id),
        "user_name": user.name,
        "discount_value": discount_info.value,
        "discount_is_temporary": 1 if discount_info.is_temporary else 0,
        "discount_is_permanent": 1 if discount_info.is_permanent else 0,
        "discount_remaining": discount_info.remaining_days,
        "balance": formatted_balance,
        "referral_balance": formatted_referral_balance,
        "referral_code": user.referral_code,
        "has_referral_balance": referral_balance > 0 and is_balance_separate,
        "is_points_reward": full_settings.referral.reward.is_money,
        "is_balance_enabled": 1 if is_balance_enabled else 0,
        "is_transfers_enabled": 1 if is_transfers_enabled else 0,
        "is_balance_separate": 1 if is_balance_separate else 0,
        "is_referral_enable": 1 if is_referral_enabled else 0,
    }

    subscription = user.current_subscription

    if not subscription:
        base_data.update(
            {
                "status": None,
                "is_trial": False,
                "trial_available": not has_used_trial and plan,
                "device_limit_bonus": 0,
            }
        )
        return base_data

    extra_devices = subscription.extra_devices or 0
    # Вычисляем бонус устройств (БЕЗ купленных доп.)
    plan_device_limit = subscription.plan.device_limit if subscription.plan.device_limit > 0 else 0
    actual_device_limit = subscription.device_limit
    device_limit_bonus = max(0, actual_device_limit - plan_device_limit - extra_devices) if plan_device_limit > 0 else 0
    
    base_data.update(
        {
            "status": subscription.get_status,
            "plan_name": subscription.plan.name,
            "current_plan_name": subscription.plan.name,
            "traffic_limit": i18n_format_traffic_limit(subscription.traffic_limit),
            "device_limit": i18n_format_device_limit(plan_device_limit if plan_device_limit > 0 else subscription.device_limit),
            "device_limit_number": plan_device_limit if plan_device_limit > 0 else subscription.device_limit,
            "device_limit_bonus": device_limit_bonus,
            "extra_devices": extra_devices,
            "expire_time": i18n_format_expire_time(subscription.expire_at),
            "is_trial": subscription.is_trial,
            "traffic_strategy": subscription.traffic_limit_strategy,
            "reset_time": subscription.get_expire_time,
        }
    )

    return base_data


@inject
async def balance_gateways_getter(
    dialog_manager: DialogManager,
    user: UserDto,
    payment_gateway_service: FromDishka[PaymentGatewayService],
    referral_service: FromDishka[ReferralService],
    settings_service: FromDishka[SettingsService],
    i18n: FromDishka[TranslatorRunner],
    **kwargs: Any,
) -> dict[str, Any]:
    from src.core.enums import PaymentGatewayType, ReferralRewardType
    
    settings = await settings_service.get()
    gateways = await payment_gateway_service.filter_active()
    referral_balance = await referral_service.get_pending_rewards_amount(
        telegram_id=user.telegram_id,
        reward_type=ReferralRewardType.MONEY,
    )
    
    payment_methods = [
        {
            "gateway_type": gateway.type,
            "name": gateway.type.value,
        }
        for gateway in gateways
        if gateway.type != PaymentGatewayType.BALANCE
    ]
    
    # Вычисляем данные о скидке пользователя
    discount_info = calculate_user_discount(user)
    
    # Извлекаем флаги из единственного объекта settings
    is_balance_enabled = settings.features.balance_enabled
    is_balance_combined = settings.features.balance_mode == BalanceMode.COMBINED
    is_balance_separate = not is_balance_combined
    is_referral_enabled = settings.referral.enable
    default_currency = settings.default_currency
    currency_rates = settings.features.currency_rates
    display_balance = get_display_balance(user.balance, referral_balance, is_balance_combined)
    
    result = {
        "payment_methods": payment_methods,
        # Данные пользователя для шапки
        "user_id": str(user.telegram_id),
        "user_name": user.name,
        "balance": format_balance(display_balance, default_currency, currency_rates),
        "referral_balance": format_balance(referral_balance, default_currency, currency_rates),
        "referral_code": user.referral_code,
        "discount_value": discount_info.value,
        "discount_is_temporary": 1 if discount_info.is_temporary else 0,
        "discount_is_permanent": 1 if discount_info.is_permanent else 0,
        "discount_remaining": discount_info.remaining_days,
        "is_balance_enabled": 1 if is_balance_enabled else 0,
        "is_balance_separate": 1 if is_balance_separate else 0,
        "is_referral_enable": 1 if is_referral_enabled else 0,
    }
    
    # Данные о текущей подписке (если есть)
    subscription = user.current_subscription
    if subscription:
        extra_devices = subscription.extra_devices or 0
        # Вычисляем бонус устройств (БЕЗ купленных доп.)
        plan_device_limit = subscription.plan.device_limit if subscription.plan.device_limit > 0 else 0
        actual_device_limit = subscription.device_limit
        device_limit_bonus = max(0, actual_device_limit - plan_device_limit - extra_devices) if plan_device_limit > 0 else 0
        
        result.update({
            "has_subscription": "true",
            "current_plan_name": subscription.plan.name,
            "plan_name": subscription.plan.name,
            "traffic_limit": i18n_format_traffic_limit(subscription.traffic_limit),
            "device_limit": i18n_format_device_limit(plan_device_limit if plan_device_limit > 0 else subscription.device_limit),
            "device_limit_number": plan_device_limit if plan_device_limit > 0 else subscription.device_limit,
            "device_limit_bonus": device_limit_bonus,
            "extra_devices": extra_devices,
            "expire_time": i18n_format_expire_time(subscription.expire_at),
        })
    else:
        result.update({
            "has_subscription": "false",
            "current_plan_name": "",
            "plan_name": "",
            "traffic_limit": "",
            "device_limit": "",
            "device_limit_number": 0,
            "device_limit_bonus": 0,
            "extra_devices": 0,
            "expire_time": "",
        })
    
    return result


@inject
async def balance_amounts_getter(
    dialog_manager: DialogManager,
    payment_gateway_service: FromDishka[PaymentGatewayService],
    settings_service: FromDishka[SettingsService],
    i18n: FromDishka[TranslatorRunner],
    **kwargs: Any,
) -> dict[str, Any]:
    from src.core.enums import PaymentGatewayType
    
    gateway_type = dialog_manager.dialog_data.get("selected_gateway")
    currency_symbol = (await settings_service.get()).default_currency.symbol
    
    # Конвертируем строку в enum если нужно
    if isinstance(gateway_type, str):
        gateway_type_enum = PaymentGatewayType(gateway_type)
    elif gateway_type:
        gateway_type_enum = gateway_type
    else:
        gateway_type_enum = None
    
    # Форматируем название способа оплаты через i18n
    if gateway_type_enum == PaymentGatewayType.YOOMONEY:
        gateway_type_formatted = i18n.get("lbl-payment-yoomoney")
    elif gateway_type_enum == PaymentGatewayType.CRYPTOMUS:
        gateway_type_formatted = i18n.get("lbl-payment-cryptomus")
    elif gateway_type_enum == PaymentGatewayType.TELEGRAM_STARS:
        gateway_type_formatted = i18n.get("lbl-payment-telegram-stars")
    elif gateway_type_enum == PaymentGatewayType.LAVA:
        gateway_type_formatted = i18n.get("lbl-payment-lava")
    elif gateway_type_enum == PaymentGatewayType.PLATEGA:
        gateway_type_formatted = i18n.get("lbl-payment-platega")
    else:
        gateway_type_formatted = gateway_type_enum.value if gateway_type_enum else "N/A"
    
    if gateway_type_enum:
        gateway = await payment_gateway_service.get_by_type(gateway_type_enum)
        if gateway:
            currency_symbol = gateway.currency.symbol
    
    return {
        "selected_gateway": gateway_type_formatted,
        "currency": currency_symbol,
    }


@inject
async def balance_amount_getter(
    dialog_manager: DialogManager,
    payment_gateway_service: FromDishka[PaymentGatewayService],
    settings_service: FromDishka[SettingsService],
    i18n: FromDishka[TranslatorRunner],
    **kwargs: Any,
) -> dict[str, Any]:
    from src.core.enums import PaymentGatewayType
    
    gateway_type = dialog_manager.dialog_data.get("selected_gateway")
    currency_symbol = (await settings_service.get()).default_currency.symbol
    
    # Конвертируем строку в enum если нужно
    if isinstance(gateway_type, str):
        gateway_type_enum = PaymentGatewayType(gateway_type)
    elif gateway_type:
        gateway_type_enum = gateway_type
    else:
        gateway_type_enum = None
    
    # Форматируем название способа оплаты через i18n
    if gateway_type_enum == PaymentGatewayType.YOOMONEY:
        gateway_type_formatted = i18n.get("lbl-payment-yoomoney")
    elif gateway_type_enum == PaymentGatewayType.CRYPTOMUS:
        gateway_type_formatted = i18n.get("lbl-payment-cryptomus")
    elif gateway_type_enum == PaymentGatewayType.TELEGRAM_STARS:
        gateway_type_formatted = i18n.get("lbl-payment-telegram-stars")
    elif gateway_type_enum == PaymentGatewayType.LAVA:
        gateway_type_formatted = i18n.get("lbl-payment-lava")
    elif gateway_type_enum == PaymentGatewayType.PLATEGA:
        gateway_type_formatted = i18n.get("lbl-payment-platega")
    else:
        gateway_type_formatted = gateway_type_enum.value if gateway_type_enum else "N/A"
    
    if gateway_type_enum:
        gateway = await payment_gateway_service.get_by_type(gateway_type_enum)
        if gateway:
            currency_symbol = gateway.currency.symbol
    
    # Получаем настройки min/max для пополнения баланса
    settings = await settings_service.get()
    min_amount = settings.features.balance_min_amount if settings.features.balance_min_amount is not None else 10
    max_amount = settings.features.balance_max_amount if settings.features.balance_max_amount is not None else 100000
    
    return {
        "selected_gateway": gateway_type_formatted,
        "currency": currency_symbol,
        "min_amount": min_amount,
        "max_amount": max_amount,
    }


@inject
async def balance_confirm_getter(
    dialog_manager: DialogManager,
    i18n: FromDishka[TranslatorRunner],
    **kwargs: Any,
) -> dict[str, Any]:
    from src.core.enums import PaymentGatewayType
    
    gateway_type = dialog_manager.dialog_data.get("selected_gateway")
    amount = dialog_manager.dialog_data.get("topup_amount", 0)
    currency = dialog_manager.dialog_data.get("currency")
    payment_url = dialog_manager.dialog_data.get("payment_url", "")
    
    # Конвертируем строку в enum если нужно
    if isinstance(gateway_type, str):
        gateway_type_enum = PaymentGatewayType(gateway_type)
    elif gateway_type:
        gateway_type_enum = gateway_type
    else:
        gateway_type_enum = None
    
    # Форматируем название способа оплаты через i18n
    if gateway_type_enum == PaymentGatewayType.YOOMONEY:
        gateway_type_formatted = i18n.get("lbl-payment-yoomoney")
    elif gateway_type_enum == PaymentGatewayType.CRYPTOMUS:
        gateway_type_formatted = i18n.get("lbl-payment-cryptomus")
    elif gateway_type_enum == PaymentGatewayType.TELEGRAM_STARS:
        gateway_type_formatted = i18n.get("lbl-payment-telegram-stars")
    elif gateway_type_enum == PaymentGatewayType.LAVA:
        gateway_type_formatted = i18n.get("lbl-payment-lava")
    elif gateway_type_enum == PaymentGatewayType.PLATEGA:
        gateway_type_formatted = i18n.get("lbl-payment-platega")
    else:
        gateway_type_formatted = gateway_type_enum.value if gateway_type_enum else "N/A"
    
    # currency может быть enum или строкой после сериализации
    if hasattr(currency, 'symbol'):
        currency_symbol = currency.symbol
    elif isinstance(currency, str) and currency in ("RUB", "USD", "EUR", "XTR"):
        from src.core.enums import Currency as CurrencyEnum
        currency_symbol = CurrencyEnum.from_code(currency).symbol
    else:
        currency_symbol = currency or "₽"
    
    return {
        "selected_gateway": gateway_type_formatted,
        "topup_amount": amount,
        "currency": currency_symbol,
        "payment_url": payment_url,
    }


@inject
async def balance_success_getter(
    dialog_manager: DialogManager,
    settings_service: FromDishka[SettingsService],
    **kwargs: Any,
) -> dict[str, Any]:
    """Getter for balance success screen."""
    start_data = dialog_manager.start_data or {}
    amount = start_data.get("amount", 0)
    default_symbol = (await settings_service.get()).default_currency.symbol
    currency = start_data.get("currency", default_symbol)
    
    return {
        "amount": amount,
        "currency": currency,
    }


@inject
async def bonus_activate_getter(
    dialog_manager: DialogManager,
    user: UserDto,
    referral_service: FromDishka[ReferralService],
    settings_service: FromDishka[SettingsService],
    **kwargs: Any,
) -> dict[str, Any]:
    from src.core.enums import ReferralRewardType
    
    # Get pending referral balance (bonuses)
    referral_balance = await referral_service.get_pending_rewards_amount(
        user.telegram_id,
        ReferralRewardType.MONEY,
    )
    
    # Если есть pending изменение суммы, показываем его
    pending_amount = dialog_manager.dialog_data.get("pending_bonus_amount")
    selected_amount = pending_amount if pending_amount else None
    
    # Вычисляем отображаемую сумму для current_bonus_amount
    if selected_amount == "all":
        display_amount = referral_balance
    elif selected_amount:
        display_amount = int(selected_amount)
    else:
        display_amount = 0
    
    # Получаем валюту для форматирования
    settings = await settings_service.get()
    default_currency = settings.default_currency
    currency_rates = settings.features.currency_rates
    
    return {
        "referral_balance": format_balance(referral_balance, default_currency, currency_rates),
        "has_balance": referral_balance > 0,
        "selected_bonus_amount": selected_amount,
        "current_bonus_amount": display_amount,
    }



@inject
async def bonus_activate_custom_getter(
    dialog_manager: DialogManager,
    user: UserDto,
    referral_service: FromDishka[ReferralService],
    settings_service: FromDishka[SettingsService],
    **kwargs: Any,
) -> dict[str, Any]:
    from src.core.enums import ReferralRewardType
    
    # Get pending referral balance
    referral_balance = await referral_service.get_pending_rewards_amount(
        user.telegram_id,
        ReferralRewardType.MONEY,
    )
    
    # Получаем валюту для форматирования
    settings = await settings_service.get()
    default_currency = settings.default_currency
    currency_rates = settings.features.currency_rates
    
    return {
        "referral_balance": format_balance(referral_balance, default_currency, currency_rates),
    }


# === Balance Transfer Getters ===


@inject
async def transfer_menu_getter(
    dialog_manager: DialogManager,
    user: UserDto,
    i18n: FromDishka[TranslatorRunner],
    settings_service: FromDishka[SettingsService],
    referral_service: FromDishka[ReferralService],
    **kwargs: Any,
) -> dict[str, Any]:
    """Геттер для меню перевода баланса."""
    from src.core.enums import ReferralRewardType
    
    settings = await settings_service.get()
    transfer_settings = settings.features.transfers
    
    # Получаем текущие данные перевода из dialog_data
    transfer_data = dialog_manager.dialog_data.get("transfer_data", {})
    recipient_id = transfer_data.get("recipient_id")
    recipient_name = transfer_data.get("recipient_name")
    transfer_amount = transfer_data.get("amount", 0)
    
    # Получаем referral_balance для расчёта отображаемого баланса
    referral_balance = await referral_service.get_pending_rewards_amount(
        user.telegram_id,
        ReferralRewardType.MONEY,
    )
    is_balance_combined = settings.features.balance_mode == BalanceMode.COMBINED
    
    # Формируем описание комиссии
    default_currency = settings.default_currency
    currency_rates = settings.features.currency_rates
    if transfer_settings.commission_type == "percent":
        commission_display = f"{int(transfer_settings.commission_value)}%"
    else:
        commission_display = format_balance(int(transfer_settings.commission_value), default_currency, currency_rates)
    
    # Формируем отображение получателя (в основном тексте)
    if recipient_id and recipient_name:
        recipient_display = f"<b>{recipient_name}</b> (<code>{recipient_id}</code>)"
    else:
        recipient_display = f"<i>{i18n.get('lbl-not-set')}</i>"
    
    # Для основного текста и кнопки - используем числовое значение
    # 0 означает "не назначено", любое другое число - назначенная сумма
    amount_display = int(transfer_amount) if transfer_amount else 0
    
    # Вычисляем комиссию для текущей суммы перевода
    transfer_commission = 0
    if transfer_amount > 0:
        if transfer_settings.commission_type == "percent":
            transfer_commission = int(transfer_amount * transfer_settings.commission_value / 100)
        else:
            transfer_commission = int(transfer_settings.commission_value)
    
    # Формируем отображение сообщения с экранированием HTML
    message = transfer_data.get("message", "")
    if message:
        # Экранируем HTML-специальные символы для безопасного отображения
        escaped_message = html.escape(message)
        message_display = f"<i>{escaped_message}</i>"
    else:
        message_display = f"<i>{i18n.get('lbl-not-set')}</i>"
    
    # Получаем валюту для форматирования баланса
    display_balance = get_display_balance(user.balance, referral_balance, is_balance_combined)
    
    return {
        "balance": format_balance(display_balance, default_currency, currency_rates),
        "commission_display": commission_display,
        "recipient_display": recipient_display,
        "amount_display": amount_display,
        "transfer_commission": transfer_commission,
        "message_display": message_display,
    }


@inject
async def transfer_recipient_getter(
    dialog_manager: DialogManager,
    **kwargs: Any,
) -> dict[str, Any]:
    """Геттер для окна ввода получателя."""
    return {}


@inject
async def transfer_recipient_history_getter(
    dialog_manager: DialogManager,
    user: UserDto,
    balance_transfer_service: FromDishka[BalanceTransferService],
    **kwargs: Any,
) -> dict[str, Any]:
    """Геттер для окна истории получателей переводов."""
    # Получаем историю уникальных получателей переводов
    recipients = await balance_transfer_service.get_transfer_recipients(
        sender_telegram_id=user.telegram_id,
        limit=20,
    )
    
    # Формируем список для отображения
    recipients_data = [
        {
            "telegram_id": r.telegram_id,
            "name": r.name or f"ID: {r.telegram_id}",
            "username": r.username,
        }
        for r in recipients
    ]
    
    return {
        "recipients": recipients_data,
        "has_recipients": len(recipients_data) > 0,
    }


@inject
async def transfer_amount_value_getter(
    dialog_manager: DialogManager,
    user: UserDto,
    i18n: FromDishka[TranslatorRunner],
    settings_service: FromDishka[SettingsService],
    referral_service: FromDishka[ReferralService],
    **kwargs: Any,
) -> dict[str, Any]:
    """Геттер для окна выбора суммы перевода."""
    from src.core.enums import ReferralRewardType
    
    settings = await settings_service.get()
    transfer_settings = settings.features.transfers
    
    # Получаем данные из dialog_data
    transfer_data = dialog_manager.dialog_data.get("transfer_data", {})
    current_amount = transfer_data.get("amount", 0)  # Текущая назначенная сумма
    pending_amount = transfer_data.get("pending_amount")  # Выбранная, но не принятая сумма
    
    # Получаем referral_balance для расчёта отображаемого баланса
    referral_balance = await referral_service.get_pending_rewards_amount(
        user.telegram_id,
        ReferralRewardType.MONEY,
    )
    is_balance_combined = settings.features.balance_mode == BalanceMode.COMBINED
    default_currency = settings.default_currency
    currency_rates = settings.features.currency_rates
    
    not_assigned = i18n.get("frg-not-assigned")
    
    # current_display - текущая назначенная сумма
    current_display = format_balance(int(current_amount), default_currency, currency_rates) if current_amount else not_assigned
    
    # selected_display - выбранная сумма (если есть pending, иначе текущая)
    display_amount = pending_amount if pending_amount is not None else current_amount
    selected_display = format_balance(int(display_amount), default_currency, currency_rates) if display_amount else not_assigned
    
    # Получаем валюту для форматирования баланса
    display_balance = get_display_balance(user.balance, referral_balance, is_balance_combined)
    
    # Создаем selected значения для всех кнопок (подсветка для pending или current)
    result = {
        "balance": format_balance(display_balance, default_currency, currency_rates),
        "min_amount": transfer_settings.min_amount if transfer_settings.min_amount else 0,
        "max_amount": transfer_settings.max_amount if transfer_settings.max_amount else 999999,
        "current_display": current_display,
        "selected_display": selected_display,
    }
    
    # Добавляем selected для preset кнопок
    for amount in [100, 250, 500, 1000, 2000, 5000]:
        result[f"amount_{amount}_selected"] = 1 if display_amount == amount else 0
    
    return result


@inject
async def transfer_amount_manual_getter(
    dialog_manager: DialogManager,
    settings_service: FromDishka[SettingsService],
    **kwargs: Any,
) -> dict[str, Any]:
    """Геттер для окна ручного ввода суммы."""
    settings = await settings_service.get()
    transfer_settings = settings.features.transfers
    
    return {
        "min_amount": transfer_settings.min_amount if transfer_settings.min_amount else 0,
        "max_amount": transfer_settings.max_amount if transfer_settings.max_amount else 999999,
    }


@inject
async def transfer_message_getter(
    dialog_manager: DialogManager,
    i18n: FromDishka[TranslatorRunner],
    **kwargs: Any,
) -> dict[str, Any]:
    """Геттер для окна ввода сообщения."""
    transfer_data = dialog_manager.dialog_data.get("transfer_data", {})
    message = transfer_data.get("message", "")
    
    if message:
        # Экранируем HTML-специальные символы для безопасного отображения
        escaped_message = html.escape(message)
        message_display = f"<i>{escaped_message}</i>"
    else:
        message_display = f"<i>{i18n.get('lbl-not-set')}</i>"
    
    return {
        "message_display": message_display,
    }

