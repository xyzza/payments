from decimal import Decimal
from payments.transfer import OperationStatusEnum


async def test_create_account(client):

    params = {
        'first_name': 'Timur',
        'last_name': 'Akhmadiev',
        'city': 'Moscow',
        'currency': 'USD'
    }

    resp = await client.post('/account', data=params)
    assert resp.status == 200
    resp = await resp.json()
    assert resp.get('account_id') == 1

    params.update({'first_name': 'Rumit', 'currency': 'USD'})
    await client.post('/account', data=params)


async def test_credit_funds(client):

    params = {'account_id': 1, 'amount': '100.00'}

    resp = await client.post('/account/credit', data=params)
    assert resp.status == 200
    resp = await resp.json()
    assert resp.get('operation_id') == 1


async def test_transfer_funds(client):

    params = {'sender_id': 1, 'recipient_id': 2, 'amount': '50.00'}

    resp = await client.post('/account/transfer', data=params)
    assert resp.status == 200
    resp = await resp.json()
    assert resp.get('operation_id') == 2


async def test_send_to_processing(client):

    resp = await client.post('processing/send', data={'operation_id': 1})
    assert resp.status == 200
    resp = await resp.json()
    assert resp['history_id']

    resp = await client.post('processing/send', data={'operation_id': 2})
    assert resp.status == 200
    resp = await resp.json()
    assert resp['history_id']


async def test_process_credit(client):

    resp = await client.post('processing/callback/credit', data={'operation_id': 1})
    assert resp.status == 200
    resp = await resp.json()
    assert resp['status'] == OperationStatusEnum.ACCEPTED


async def test_process_transfer(client):

    resp = await client.post('processing/callback/transfer', data={'operation_id': 2})
    assert resp.status == 200
    resp = await resp.json()
    assert resp['status'] == OperationStatusEnum.ACCEPTED


async def test_check_balance(client):

    resp = await client.get('/account/balance', params={'account_id': 1})
    assert resp.status == 200
    resp = await resp.json()
    assert Decimal(resp['account_balance']) == Decimal('50.00')

    resp = await client.get('/account/balance', params={'account_id': 2})
    assert resp.status == 200
    resp = await resp.json()
    assert Decimal(resp['account_balance']) == Decimal('50.00')


async def test_report(client):

    resp = await client.get('/report', params={
        'first_name': 'Timur',
        'last_name': 'Akhmadiev',
        'begin': '',
        'end': ''
    })

    assert resp.status == 200
    resp = await resp.json()
    assert len(resp.get('rows', [])) == 6
