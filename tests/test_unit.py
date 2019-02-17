from decimal import Decimal
from payments.account import CurrencyEnum
from payments.account import convert_currency


def test_convert_currency():

    converted = convert_currency(
        Decimal('42.42'),
        CurrencyEnum.EUR,
        CurrencyEnum.USD
    )

    assert converted == Decimal('0.00')
