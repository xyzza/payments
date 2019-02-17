import pytest
from decimal import Decimal
from payments.account import create_account
from payments.account import account_balance
from payments.account import CurrencyEnum
from payments.processing import process_credit_operation, \
    process_transfer_operation
from payments.transfer import crediting_funds, transfer_funds
from payments.transfer import send_to_processing
from payments.transfer import OperationStatusEnum


@pytest.fixture()
def sender_account_id():
    return 1


@pytest.fixture()
def recipient_account_id():
    return 1


def test_create_account():

    account_id = create_account('Tim', 'Akhmadiev', 'Kazan', CurrencyEnum.USD)

    assert account_id == 1


def test_crediting_funds(sender_account_id):

    old_balance = account_balance(sender_account_id)
    amount = Decimal('42.42')

    operation_id = crediting_funds(sender_account_id, amount, CurrencyEnum.EUR)

    operations_processed = send_to_processing()
    assert operations_processed == 1

    status = process_credit_operation(operation_id)
    assert status == OperationStatusEnum.ACCEPTED

    new_balance = account_balance(sender_account_id)
    assert old_balance + amount == new_balance


def test_transfer_funds(sender_account_id, recipient_account_id):

    amount = Decimal('42.42')

    operation_id = transfer_funds(sender_account_id, recipient_account_id, amount)

    operations_processed = send_to_processing()
    assert operations_processed == 1

    status = process_transfer_operation(operation_id)
    assert status == OperationStatusEnum.ACCEPTED
