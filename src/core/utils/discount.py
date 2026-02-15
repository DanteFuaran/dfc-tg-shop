"""Утилиты для расчёта скидок пользователя."""
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.services.dto import UserDto


@dataclass
class DiscountInfo:
    """Информация о скидке пользователя."""
    
    value: int
    is_temporary: bool
    is_permanent: bool
    remaining_days: int


def calculate_user_discount(user: "UserDto") -> DiscountInfo:
    """
    Вычисляет данные о скидке пользователя.
    
    Логика:
    - Временная скидка (purchase_discount) имеет приоритет если она больше постоянной
    - Постоянная скидка (personal_discount) используется если она больше или временная истекла
    - Временная скидка считается активной только если не истекла
    
    Returns:
        DiscountInfo с полями:
        - value: итоговая скидка в процентах
        - is_temporary: True если активная скидка временная
        - is_permanent: True если активная скидка постоянная
        - remaining_days: оставшиеся дни для временной скидки (0 если постоянная)
    """
    purchase_disc = user.purchase_discount if user.purchase_discount is not None else 0
    personal_disc = user.personal_discount if user.personal_discount is not None else 0
    
    discount_remaining = 0
    is_temporary_discount = False
    is_permanent_discount = False
    discount_value = 0
    
    # Проверяем временную скидку
    if purchase_disc > 0 and user.purchase_discount_expires_at is not None:
        now = datetime.now(timezone.utc)
        if user.purchase_discount_expires_at <= now:
            # Временная скидка истекла
            purchase_disc = 0
        else:
            # Временная скидка активна
            remaining = user.purchase_discount_expires_at - now
            discount_remaining = remaining.days + (1 if remaining.seconds > 0 else 0)
            is_temporary_discount = True
    
    # Определяем итоговую скидку
    if purchase_disc > 0 or personal_disc > 0:
        if purchase_disc > personal_disc:
            discount_value = purchase_disc
        elif personal_disc > 0:
            discount_value = personal_disc
            is_temporary_discount = False
            is_permanent_discount = True
            discount_remaining = 0
        else:
            discount_value = purchase_disc
    
    return DiscountInfo(
        value=discount_value,
        is_temporary=is_temporary_discount,
        is_permanent=is_permanent_discount,
        remaining_days=discount_remaining,
    )
