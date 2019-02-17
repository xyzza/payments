from decimal import Decimal
from payments.account import CurrencyEnum


class OperationStatusEnum:

    DRAFT = 'DRAFT'
    PROCESSING = 'PROCESSING'
    ACCEPTED = 'ACCEPTED'
    FAILED = 'FAILED'


def crediting_funds(account_id: int, amount: Decimal, currency: CurrencyEnum) -> int:
    raise NotImplementedError()
    return 'operation id'


def transfer_funds(sender_account_id: int, recipient_account_id: int, amount: Decimal) -> int:
    raise NotImplementedError()
    return 'operation id'


def send_to_processing():
    """
        Выбираем все DRAFT и отправляем в PROCESSING
    :return:
    """
    raise NotImplementedError()
    return 'number_of_processed operations'
