import psycopg2
from decimal import Decimal
from payments.converter import CurrencyEnum


async def create_account(
        pool,
        first_name: str,
        last_name: str,
        city: str,
        currency: CurrencyEnum) -> int:

    query = """
    INSERT INTO account
        (first_name, last_name, country, currency)
    VALUES ($1, $2, $3, $4) RETURNING id;
    """

    params = (first_name, last_name, city, currency)

    try:
        async with pool.acquire(timeout=10) as conn:
            result = await conn.fetchval(query, *params)
    except psycopg2.IntegrityError:
        raise Exception('account already exists')

    return result


async def account_balance(pool, account_id: int) -> Decimal:

    query = """
    SELECT balance FROM account WHERE id = $1
    """
    params = (int(account_id), )
    # TODO: timeout to settings
    async with pool.acquire(timeout=10) as conn:
        result = await conn.fetchval(query, *params)

    return result
