from decimal import Decimal

from payments.converter import CurrencyEnum
from payments.converter import convert_currency


def test_convert_usd_usd():

    converted = convert_currency(
        Decimal('42.42'),
        CurrencyEnum.USD,
        CurrencyEnum.USD
    )

    assert converted == Decimal('42.42')


def test_convert_usd_eur():

    converted = convert_currency(
        Decimal('10'),
        CurrencyEnum.USD,
        CurrencyEnum.EUR
    )

    assert converted == Decimal('8.80')


def test_convert_usd_cad():

    converted = convert_currency(
        Decimal('10'),
        CurrencyEnum.USD,
        CurrencyEnum.CAD
    )

    assert converted == Decimal('13.20')


def test_convert_usd_cny():

    converted = convert_currency(
        Decimal('10'),
        CurrencyEnum.USD,
        CurrencyEnum.CNY
    )

    assert converted == Decimal('67.60')


def test_convert_eur_usd():

    converted = convert_currency(
        Decimal('10'),
        CurrencyEnum.EUR,
        CurrencyEnum.USD
    )

    assert converted == Decimal('11.20')


def test_convert_cad_usd():

    converted = convert_currency(
        Decimal('10'),
        CurrencyEnum.CAD,
        CurrencyEnum.USD
    )

    assert converted == Decimal('7.50')


def test_convert_cny_usd():

    converted = convert_currency(
        Decimal('10'),
        CurrencyEnum.CNY,
        CurrencyEnum.USD
    )

    assert converted == Decimal('1.40')


def test_eur_to_cad():

    converted = convert_currency(
        Decimal('10'),
        CurrencyEnum.EUR,
        CurrencyEnum.CAD
    )

    assert converted == Decimal('14.78')
