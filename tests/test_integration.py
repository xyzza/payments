from decimal import Decimal
from datetime import datetime
from datetime import timedelta

from payments.operation import OperationStatusEnum


async def test_create_account(client):

    params = {
        'first_name': 'Timur',
        'last_name': 'Akhmadiev',
        'city': 'Moscow',
        'currency': 'USD'
    }

    resp = await client.post('/account/create', data=params)
    assert resp.status == 200
    resp = await resp.json()
    assert resp.get('account_id') == 1

    params.update({'first_name': 'Rumit', 'currency': 'USD'})
    await client.post('/account/create', data=params)


async def test_create_existing_account(client):

    params = {
        'first_name': 'Timur',
        'last_name': 'Akhmadiev',
        'city': 'Moscow',
        'currency': 'USD'
    }

    resp = await client.post('/account/create', data=params)
    assert resp.status == 422
    resp = await resp.json()
    assert resp.get('error') == 'Account already exists'


async def test_credit_funds(client):

    params = {'account_id': 1, 'amount': '100.00'}

    resp = await client.post('/transfers/credit', data=params)
    assert resp.status == 202
    resp = await resp.json()
    assert resp.get('operation_id') == 1

    resp = await client.post('processing/send', data={'operation_id': 1})
    assert resp.status == 202
    resp = await resp.json()
    assert resp['history_id']

    resp = await client.post('processing/callback/credit', data={'operation_id': 1})
    assert resp.status == 200
    resp = await resp.json()
    assert resp['status'] == OperationStatusEnum.ACCEPTED


async def test_transfer_funds(client):

    params = {'sender_id': 1, 'recipient_id': 2, 'amount': '60.00'}

    resp = await client.post('/transfers/transfer', data=params)
    assert resp.status == 202
    resp = await resp.json()
    assert resp.get('operation_id') == 2

    params = {'sender_id': 2, 'recipient_id': 1, 'amount': '20.00'}

    resp = await client.post('/transfers/transfer', data=params)
    assert resp.status == 422
    resp = await resp.json()
    assert resp.get('error') == 'Not enough funds to transfer'


async def test_transfer_funds_account_doesnt_exists(client):

    params = {'sender_id': 1, 'recipient_id': 2000, 'amount': '50.00'}

    resp = await client.post('/transfers/transfer', data=params)
    assert resp.status == 404
    resp = await resp.json()
    assert resp.get('error') == 'Account not found'

    params = {'sender_id': 1000, 'recipient_id': 2000, 'amount': '50.00'}

    resp = await client.post('/transfers/transfer', data=params)
    assert resp.status == 404
    resp = await resp.json()
    assert resp.get('error') == 'Account not found'


async def test_send_to_processing(client):

    resp = await client.post('processing/send', data={'operation_id': 2})
    assert resp.status == 202
    resp = await resp.json()
    assert resp['history_id']


async def test_send_to_processing_twice(client):

    resp = await client.post('processing/send', data={'operation_id': 2})
    assert resp.status == 422
    resp = await resp.json()
    assert resp.get('error') == 'Operation inconsistent'


async def test_send_to_processing_non_existing(client):

    resp = await client.post('processing/send', data={'operation_id': 1000})
    assert resp.status == 404
    resp = await resp.json()
    assert resp.get('error') == 'Operation not found'


async def test_process_wrong_credit(client):
    """Try to credit "transfer" operation"""
    resp = await client.post('processing/callback/credit', data={'operation_id': 2})
    assert resp.status == 404
    resp = await resp.json()
    assert resp.get('error') == 'Operation not found'


async def test_process_wrong_transfer(client):
    """Try to transfer "credit" operation"""
    resp = await client.post('processing/callback/transfer', data={'operation_id': 1})
    assert resp.status == 404
    resp = await resp.json()
    assert resp.get('error') == 'Operation not found'


async def test_process_transfer(client):

    resp = await client.post('processing/callback/transfer', data={'operation_id': 2})
    assert resp.status == 200
    resp = await resp.json()
    assert resp['status'] == OperationStatusEnum.ACCEPTED


async def test_process_operation_twice(client):

    resp = await client.post('processing/callback/transfer', data={'operation_id': 2})
    assert resp.status == 422
    resp = await resp.json()
    assert resp.get('error') == 'Operation inconsistent'

    resp = await client.post('processing/callback/credit', data={'operation_id': 1})
    assert resp.status == 422
    resp = await resp.json()
    assert resp.get('error') == 'Operation inconsistent'


async def test_check_balance(client):

    resp = await client.get('/account/balance', params={'account_id': 1})
    assert resp.status == 200
    resp = await resp.json()
    assert Decimal(resp['account_balance']) == Decimal('40.00')

    resp = await client.get('/account/balance', params={'account_id': 2})
    assert resp.status == 200
    resp = await resp.json()
    assert Decimal(resp['account_balance']) == Decimal('60.00')


async def test_check_balance_account_doesnt_exists(client):

    resp = await client.get('/account/balance', params={'account_id': 1000})
    assert resp.status == 404
    resp = await resp.json()
    assert resp.get('error') == 'Account not found'


async def test_report(client):

    start_time = datetime.now()

    params = {'sender_id': 2, 'recipient_id': 1, 'amount': '25.00'}

    resp = await client.post('/transfers/transfer', data=params)
    assert resp.status == 202
    resp = await resp.json()
    assert resp.get('operation_id') == 3

    resp = await client.post('processing/send', data={'operation_id': 3})
    assert resp.status == 202
    resp = await resp.json()
    assert resp['history_id']

    resp = await client.post('processing/callback/transfer', data={'operation_id': 3})
    assert resp.status == 200
    resp = await resp.json()
    assert resp['status'] == OperationStatusEnum.ACCEPTED

    end_time = datetime.now()

    resp = await client.get('/report', params={
        'first_name': 'Timur',
        'last_name': 'Akhmadiev',
        'begin': start_time.strftime('%Y-%m-%d %H:%M:%S.%f'),
        'end': end_time.strftime('%Y-%m-%d %H:%M:%S.%f')
    })

    assert resp.status == 200
    resp = await resp.json()
    assert len(resp.get('rows', [])) == 3

    prev_day = start_time - timedelta(1)

    resp = await client.get('/report', params={
        'first_name': 'Timur',
        'last_name': 'Akhmadiev',
        'begin': prev_day.strftime('%Y-%m-%d %H:%M:%S.%f'),
    })

    assert resp.status == 200
    resp = await resp.json()
    assert len(resp.get('rows', [])) == 9

    resp = await client.get('/report', params={
        'first_name': 'Timur',
        'last_name': 'Akhmadiev',
        'end': start_time.strftime('%Y-%m-%d %H:%M:%S.%f'),
    })

    assert resp.status == 200
    resp = await resp.json()
    assert len(resp.get('rows', [])) == 6

    resp = await client.get('/report', params={
        'first_name': 'Timur',
        'last_name': 'Akhmadiev',
    })

    assert resp.status == 200
    resp = await resp.json()
    assert len(resp.get('rows', [])) == 9


async def test_report_user_not_found(client):

    resp = await client.get('/report', params={
        'first_name': 'User',
        'last_name': 'Unknown',
    })

    assert resp.status == 404
    resp = await resp.json()
    assert resp.get('error') == 'Account not found'


async def test_report_no_operations(client):

    params = {
        'first_name': 'User',
        'last_name': 'NoOperation',
        'city': 'Moscow',
        'currency': 'USD'
    }

    resp = await client.post('/account/create', data=params)
    assert resp.status == 200

    resp = await client.get('/report', params={
        'first_name': 'User',
        'last_name': 'NoOperation',
    })

    assert resp.status == 200
    resp = await resp.json()
    assert len(resp.get('rows')) == 0
