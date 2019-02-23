import psycopg2
import pytest
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from yoyo import get_backend
from yoyo import read_migrations

from payments import settings
from payments.server import init_app
from payments.server import init_db


@pytest.fixture(scope='session')
def db_test_setup_teardown():

    dsn = settings.DB_DSN.split('/')
    db_name = dsn.pop()
    db_name = f'testing_database_{db_name}'
    dsn = '/'.join(dsn)

    with psycopg2.connect(dsn) as conn:
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cursor:
            cursor.execute(f'DROP DATABASE IF EXISTS {db_name}')
            cursor.execute(f'CREATE DATABASE {db_name}')

    new_dsn = f'{dsn}/{db_name}'

    backend = get_backend(new_dsn)
    migrations = read_migrations('payments/db/migrations')
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))

    yield new_dsn


@pytest.fixture()
def db(db_test_setup_teardown):
    return init_db(db_test_setup_teardown, settings.DB_POOL_SIZE)


@pytest.fixture()
def app(db):
    return init_app(db)


@pytest.fixture()
async def client(aiohttp_client, app):
    return await aiohttp_client(app)
