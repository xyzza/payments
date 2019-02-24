from decimal import Decimal

import asyncpg

from payments import settings
from payments.converter import CurrencyEnum

from .exceptions import AccountAlreadyExistsError
from .exceptions import AccountDoesNotExistsError
from .query import account_balance as _account_balance
from .query import account_balances_pair as _account_balances_pair
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
        raise AccountAlreadyExistsError()

    return account_id


async def account_balance(pool, account_id: int) -> Decimal:

    async with pool.acquire(timeout=settings.DB_TIMEOUT) as conn:
        result = await conn.fetchval(_account_balance, account_id)

    if result is None:
        raise AccountDoesNotExistsError()

    return result


async def account_balances_pair(pool, sender_id, recipient_id):

    async with pool.acquire(timeout=settings.DB_TIMEOUT) as conn:
        try:
            sender_balance, recipient_balance = await conn.fetch(
                _account_balances_pair,
                sender_id,
                recipient_id
            )
        except ValueError:
            raise AccountDoesNotExistsError()

    return sender_balance[0], recipient_balance[0]
