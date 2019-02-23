from decimal import Decimal

import asyncpg

from payments import settings
from payments.converter import CurrencyEnum

from .exceptions import AccountAlreadyExists
from .exceptions import AccountDoesNotExists
from .query import account_balance as _account_balance
from .query import create_account as _create_account


async def create_account(
        pool,
        first_name: str,
        last_name: str,
        city: str,
        currency: CurrencyEnum) -> int:

    try:
        async with pool.acquire(timeout=settings.DB_TIMEOUT) as conn:
            account_id = await conn.fetchval(
                _create_account,
                first_name,
                last_name,
                city,
                currency
            )
    except asyncpg.exceptions.UniqueViolationError:
        raise AccountAlreadyExists()

    return account_id


async def account_balance(pool, account_id: int) -> Decimal:

    async with pool.acquire(timeout=settings.DB_TIMEOUT) as conn:
        result = await conn.fetchval(_account_balance, account_id)

    if result is None:
        raise AccountDoesNotExists()

    return result
