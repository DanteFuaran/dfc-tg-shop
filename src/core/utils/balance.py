"""Утилиты для работы с балансом пользователя."""

from decimal import Decimal, ROUND_DOWN

from src.core.enums import Currency
from src.core.utils.formatters import format_price


def get_display_balance(user_balance: int, referral_balance: int, is_combined: bool) -> int:
    """
    Вычисляет отображаемый баланс пользователя.
    
    Args:
        user_balance: Основной баланс пользователя
        referral_balance: Реферальный баланс (накопленные бонусы)
        is_combined: True если балансы объединены в один
        
    Returns:
        Итоговый баланс для отображения
    """
    return user_balance + referral_balance if is_combined else user_balance


def convert_balance(amount_rub: int, currency: Currency, currency_rates) -> Decimal:
    """
    Конвертирует сумму из рублей в целевую валюту по курсу из настроек.
    
    Args:
        amount_rub: Сумма в рублях
        currency: Целевая валюта
        currency_rates: CurrencyRatesDto с курсами валют
        
    Returns:
        Сконвертированная сумма
    """
    if currency == Currency.RUB or amount_rub == 0:
        return Decimal(amount_rub)
    
    amount = Decimal(amount_rub)
    
    match currency:
        case Currency.XTR:
            result = amount / Decimal(str(currency_rates.stars_rate))
            return result.to_integral_value(rounding=ROUND_DOWN)
        case Currency.USD:
            result = amount / Decimal(str(currency_rates.usd_rate))
            return result.quantize(Decimal("0.01"))
        case Currency.EUR:
            result = amount / Decimal(str(currency_rates.eur_rate))
            return result.quantize(Decimal("0.01"))
        case _:
            return Decimal(amount_rub)


def format_balance(amount_rub: int, currency: Currency, currency_rates=None) -> str:
    """
    Форматирует баланс с конвертацией из рублей в целевую валюту.
    
    Баланс хранится в рублях. При отображении конвертируется
    по курсу из настроек и форматируется с символом валюты.
    
    Args:
        amount_rub: Сумма в рублях
        currency: Целевая валюта для отображения
        currency_rates: CurrencyRatesDto с курсами валют
        
    Returns:
        Отформатированная строка ("100 ₽", "67 ★", "1.11 $")
    """
    if currency == Currency.RUB or not currency_rates:
        return format_price(amount_rub, Currency.RUB)
    
    converted = convert_balance(amount_rub, currency, currency_rates)
    return format_price(converted, currency)
