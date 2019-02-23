from decimal import Decimal


class CurrencyEnum:

    USD = 'USD'
    EUR = 'EUR'
    CAD = 'CAD'
    CNY = 'CNY'

    values = ('USD', 'EUR', 'CAD', 'CNY')

    exchange_rates = {
        (USD, USD): Decimal('1.00'),

        (USD, EUR): Decimal('0.88'),
        (USD, CAD): Decimal('1.32'),
        (USD, CNY): Decimal('6.76'),

        (EUR, USD): Decimal('1.12'),
        (CAD, USD): Decimal('0.75'),
        (CNY, USD): Decimal('0.14'),
    }


def convert_currency(amount: Decimal,
                     from_currency: CurrencyEnum,
                     to_currency: CurrencyEnum) -> Decimal:

    assert from_currency in CurrencyEnum.values
    assert to_currency in CurrencyEnum.values

    try:
        rate = CurrencyEnum.exchange_rates[from_currency, to_currency]
        converted = round(amount * rate, 2)

    except KeyError:
        usd = convert_currency(amount, from_currency, CurrencyEnum.USD)
        converted = convert_currency(usd, CurrencyEnum.USD, to_currency)

    return converted
