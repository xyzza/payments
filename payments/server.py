from aiohttp import web

from payments import settings
from payments.account import balance_view
from payments.account import create_view
from payments.db import create_pool
from payments.processing import process_credit_view
from payments.processing import process_transfer_view
from payments.processing import process_view
from payments.report import report_view
from payments.transfer import credit_view
from payments.transfer import transfer_view


def init_app(db):

    async def _pool_on_startup(app):
        app['db'] = await db

    async def _db_pool_cleanup(app):
        await app['db'].close()

    app = web.Application()

    app.router.add_post('/account/create', create_view)
    app.router.add_get('/account/balance', balance_view)

    app.router.add_post('/transfers/credit', credit_view)
    app.router.add_post('/transfers/transfer', transfer_view)

    app.router.add_post('/processing/send', process_view)
    app.router.add_post('/processing/callback/credit', process_credit_view)
    app.router.add_post('/processing/callback/transfer', process_transfer_view)

    app.router.add_get('/report', report_view)

    app.on_startup.append(_pool_on_startup)
    app.on_cleanup.append(_db_pool_cleanup)

    return app


def init_db(dsn, pool_size):
    return create_pool(dsn, pool_size)


def run_app():
    app = init_app(init_db(settings.DB_DSN, settings.DB_POOL_SIZE))
    web.run_app(app)
