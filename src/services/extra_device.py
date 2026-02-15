"""Сервис для управления покупками дополнительных устройств."""

from datetime import datetime, timedelta
from typing import Optional

from aiogram import Bot
from fluentogram import TranslatorHub
from loguru import logger
from redis.asyncio import Redis

from src.core.config import AppConfig
from src.core.utils.time import datetime_now
from src.infrastructure.database import UnitOfWork
from src.infrastructure.database.models.dto import ExtraDevicePurchaseDto, SubscriptionDto, UserDto
from src.infrastructure.database.models.sql import ExtraDevicePurchase
from src.infrastructure.redis import RedisRepository

from .base import BaseService


class ExtraDeviceService(BaseService):
    """Сервис для работы с дополнительными устройствами."""
    
    uow: UnitOfWork

    def __init__(
        self,
        config: AppConfig,
        bot: Bot,
        redis_client: Redis,
        redis_repository: RedisRepository,
        translator_hub: TranslatorHub,
        uow: UnitOfWork,
    ) -> None:
        super().__init__(config, bot, redis_client, redis_repository, translator_hub)
        self.uow = uow

    async def create_purchase(
        self,
        user: UserDto,
        subscription: SubscriptionDto,
        device_count: int,
        price: int,
        duration_days: int = 30,
    ) -> list[ExtraDevicePurchaseDto]:
        """
        Создать покупку дополнительных устройств.
        
        Каждое устройство создаётся как отдельная запись с device_count=1.
        Это упрощает логику удаления - каждое устройство можно пометить на удаление отдельно.
        """
        now = datetime_now()
        expires_at = now + timedelta(days=duration_days)
        price_per_device = price // device_count if device_count > 0 else price
        
        created_purchases = []
        
        for i in range(device_count):
            purchase = ExtraDevicePurchase(
                subscription_id=subscription.id,
                user_telegram_id=user.telegram_id,
                device_count=1,  # Всегда 1 устройство на запись
                price=price_per_device,
                is_active=True,
                auto_renew=True,
                purchased_at=now,
                expires_at=expires_at,
            )
            
            created = await self.uow.repository.extra_device_purchases.create(purchase)
            created_purchases.append(self._to_dto(created))
        
        await self.uow.commit()
        
        logger.info(
            f"Created {device_count} extra device purchase(s) for user '{user.telegram_id}': "
            f"price_per_device={price_per_device}, expires_at={expires_at}"
        )
        
        return created_purchases

    async def get(self, purchase_id: int) -> Optional[ExtraDevicePurchaseDto]:
        """Получить покупку по ID."""
        purchase = await self.uow.repository.extra_device_purchases.get(purchase_id)
        return self._to_dto(purchase) if purchase else None

    async def get_by_subscription(self, subscription_id: int) -> list[ExtraDevicePurchaseDto]:
        """Получить все покупки для подписки."""
        purchases = await self.uow.repository.extra_device_purchases.get_by_subscription(subscription_id)
        return [self._to_dto(p) for p in purchases]

    async def get_active_by_subscription(self, subscription_id: int) -> list[ExtraDevicePurchaseDto]:
        """Получить активные покупки для подписки."""
        purchases = await self.uow.repository.extra_device_purchases.get_active_by_subscription(subscription_id)
        return [self._to_dto(p) for p in purchases]

    async def get_by_user(self, telegram_id: int) -> list[ExtraDevicePurchaseDto]:
        """Получить все покупки пользователя."""
        purchases = await self.uow.repository.extra_device_purchases.get_by_user(telegram_id)
        return [self._to_dto(p) for p in purchases]

    async def get_active_by_user(self, telegram_id: int) -> list[ExtraDevicePurchaseDto]:
        """Получить активные покупки пользователя."""
        purchases = await self.uow.repository.extra_device_purchases.get_active_by_user(telegram_id)
        return [self._to_dto(p) for p in purchases]

    async def get_total_active_devices(self, subscription_id: int) -> int:
        """Получить общее количество активных дополнительных устройств."""
        return await self.uow.repository.extra_device_purchases.get_total_active_devices(subscription_id)

    async def get_total_monthly_cost(self, subscription_id: int) -> int:
        """Получить общую месячную стоимость дополнительных устройств."""
        return await self.uow.repository.extra_device_purchases.get_total_monthly_cost(subscription_id)

    async def disable_auto_renew(self, purchase_id: int) -> Optional[ExtraDevicePurchaseDto]:
        """Отключить автопродление для покупки."""
        purchase = await self.uow.repository.extra_device_purchases.disable_auto_renew(purchase_id)
        if purchase:
            await self.uow.commit()
            logger.info(f"Disabled auto-renew for extra device purchase '{purchase_id}'")
        return self._to_dto(purchase) if purchase else None

    async def deactivate(self, purchase_id: int) -> Optional[ExtraDevicePurchaseDto]:
        """Деактивировать покупку (устройства будут удалены)."""
        purchase = await self.uow.repository.extra_device_purchases.deactivate(purchase_id)
        if purchase:
            await self.uow.commit()
            logger.info(f"Deactivated extra device purchase '{purchase_id}'")
        return self._to_dto(purchase) if purchase else None

    async def mark_for_deletion(self, purchase_id: int) -> Optional[ExtraDevicePurchaseDto]:
        """Пометить покупку на удаление (будет удалена по истечении срока)."""
        purchase = await self.uow.repository.extra_device_purchases.update(
            purchase_id,
            pending_deletion=True,
            auto_renew=False,  # Отключаем автопродление
        )
        if purchase:
            await self.uow.commit()
            logger.info(f"Marked extra device purchase '{purchase_id}' for deletion")
        return self._to_dto(purchase) if purchase else None

    async def delete(self, purchase_id: int) -> bool:
        """Полностью удалить покупку."""
        result = await self.uow.repository.extra_device_purchases.delete(purchase_id)
        if result:
            await self.uow.commit()
            logger.info(f"Deleted extra device purchase '{purchase_id}'")
        return result

    async def renew_purchase(
        self,
        purchase_id: int,
        duration_days: int = 30,
    ) -> Optional[ExtraDevicePurchaseDto]:
        """Продлить срок действия покупки."""
        purchase = await self.uow.repository.extra_device_purchases.get(purchase_id)
        if not purchase:
            return None
        
        # Продлеваем от текущей даты истечения или от сейчас
        now = datetime_now()
        base_date = max(purchase.expires_at, now)
        new_expires_at = base_date + timedelta(days=duration_days)
        
        updated = await self.uow.repository.extra_device_purchases.update(
            purchase_id,
            expires_at=new_expires_at,
            is_active=True,
        )
        
        if updated:
            await self.uow.commit()
            logger.info(
                f"Renewed extra device purchase '{purchase_id}': "
                f"new_expires_at={new_expires_at}"
            )
        
        return self._to_dto(updated) if updated else None

    async def get_expired_active_purchases(self) -> list[ExtraDevicePurchaseDto]:
        """Получить истекшие, но ещё активные покупки."""
        purchases = await self.uow.repository.extra_device_purchases.get_expired_active()
        return [self._to_dto(p) for p in purchases]

    async def get_expiring_soon(self, hours: int = 24) -> list[ExtraDevicePurchaseDto]:
        """Получить покупки, истекающие в ближайшие N часов."""
        expires_before = datetime_now() + timedelta(hours=hours)
        purchases = await self.uow.repository.extra_device_purchases.get_expiring_soon(expires_before)
        return [self._to_dto(p) for p in purchases]

    @staticmethod
    def _to_dto(purchase: Optional[ExtraDevicePurchase]) -> Optional[ExtraDevicePurchaseDto]:
        """Конвертировать SQL модель в DTO."""
        if not purchase:
            return None
        return ExtraDevicePurchaseDto(
            id=purchase.id,
            subscription_id=purchase.subscription_id,
            user_telegram_id=purchase.user_telegram_id,
            device_count=purchase.device_count,
            price=purchase.price,
            is_active=purchase.is_active,
            auto_renew=purchase.auto_renew,
            pending_deletion=purchase.pending_deletion,
            purchased_at=purchase.purchased_at,
            expires_at=purchase.expires_at,
            created_at=purchase.created_at,
            updated_at=purchase.updated_at,
        )
