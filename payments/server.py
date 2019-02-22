from decimal import Decimal

from aiohttp import ClientSession
from aiohttp import web

from payments import settings
from payments.account import account_balance
from payments.account import create_account
from payments.db import create_pool
from payments.processing import process_credit_operation
from payments.processing import process_transfer_operation
from payments.report import billing_report
from payments.report.schema import report_schema
from payments.transfer import credit_funds
from payments.transfer import send_to_processing
from payments.transfer import transfer_funds


async def create(request):

    data = await request.post()

    result = await create_account(
        request.app['db'],
        data['first_name'],
        data['last_name'],
        data['city'],
        data['currency']
    )

    return web.json_response({'account_id': result})


async def balance(request):

    data = request.rel_url.query

    result = await account_balance(
        request.app['db'],
        data['account_id']
    )

    return web.json_response({'account_balance': str(result)})


async def credit(request):

    data = await request.post()

    operation_id = await credit_funds(
        request.app['db'],
        data['account_id'],
        Decimal(data['amount'])
    )

    return web.json_response({'operation_id': operation_id})


async def transfer(request):

    data = await request.post()

    operation_id = await transfer_funds(
        request.app['db'],
        data['sender_id'],
        data['recipient_id'],
        Decimal(data['amount'])
    )

    return web.json_response({'operation_id': operation_id})


async def process(request):

    data = await request.post()

    history_id = await send_to_processing(
        request.app['db'],
        data['operation_id']
    )

    return web.json_response({'history_id': history_id})


async def process_credit(request):

    data = await request.post()

    operation_status = await process_credit_operation(
        request.app['db'],
        data['operation_id']
    )

    return web.json_response({'status': operation_status})


async def process_transfer(request):

    data = await request.post()

    operation_status = await process_transfer_operation(
        request.app['db'],
        data['operation_id']
    )

    return web.json_response({'status': operation_status})


async def report(request):

    data = request.rel_url.query

    rows = await billing_report(
        request.app['db'],
        data['first_name'],
        data['last_name'],
        data['begin'],
        data['end']
    )

    rows = [report_schema.dump(r) for r in rows]

    return web.json_response({'rows': rows})


def init_app(db, session):

    async def _pool_on_startup(app):
        app['db'] = await db

    async def _db_pool_cleanup(app):
        await app['db'].close()

    async def _session_cleanup(app):
        await app['session'].close()

    app = web.Application()
    app.router.add_post('/account', create)
    app.router.add_post('/account/credit', credit)
    app.router.add_post('/account/transfer', transfer)
    app.router.add_get('/account/balance', balance)
    app.router.add_post('/processing/send', process)
    app.router.add_post('/processing/callback/credit', process_credit)
    app.router.add_post('/processing/callback/transfer', process_transfer)
    app.router.add_get('/report', report)

    app['session'] = session

    app.on_startup.append(_pool_on_startup)
    app.on_cleanup.extend([_db_pool_cleanup, _session_cleanup])

    return app


def init_session():
    return ClientSession()


def init_db(dsn, pool_size):
    return create_pool(dsn, pool_size)


def run_app():
    session = init_session()
    app = init_app(init_db(settings.DB_DSN, settings.DB_POOL_SIZE), session)
    web.run_app(app)
