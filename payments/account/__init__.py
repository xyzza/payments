from decimal import Decimal


class CurrencyEnum:

    USD = 'USD'
    EUR = 'UER'


def create_account(first_name: str, last_name: str, city: str, currency: CurrencyEnum) -> int:
    raise NotImplementedError()
    return 'account_id' # номер кошелька клиента


def account_balance(account_id: int) -> Decimal:
    raise NotImplementedError()
    return Decimal('0.00')


def convert_currency(amount: Decimal, from_currency: CurrencyEnum, to_currency: CurrencyEnum) -> Decimal:
    raise NotImplementedError()
    return Decimal('0.00')
