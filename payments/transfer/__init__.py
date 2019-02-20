from decimal import Decimal

from payments.converter import convert_currency


class OperationStatusEnum:

    DRAFT = 'DRAFT'
    PROCESSING = 'PROCESSING'
    ACCEPTED = 'ACCEPTED'
    FAILED = 'FAILED'


async def credit_funds(pool, account_id: int, amount: Decimal) -> int:

    async with pool.acquire(timeout=10) as conn:
        async with conn.transaction():

            query = """
            INSERT INTO operation
                (sender_id, recipient_id, volume)
            VALUES ($1, $2, $3) RETURNING id;
            """
            params = (int(account_id), int(account_id), Decimal(amount))
            operation_id = await conn.fetchval(query, *params)

            query = """
            INSERT INTO operation_history
                (operation_id)
            VALUES ($1);
            """
            params = (operation_id, )
            await conn.execute(query, *params)

    return operation_id


async def transfer_funds(
        pool,
        sender_account_id: int,
        recipient_account_id: int,
        amount: Decimal) -> int:
    # TODO: timeout to settings
    async with pool.acquire(timeout=10) as conn:
        async with conn.transaction():

            query = """
            INSERT INTO operation
                (sender_id, recipient_id, volume)
            VALUES ($1, $2, $3) RETURNING id;
            """

            params = (
                int(sender_account_id),
                int(recipient_account_id),
                Decimal(amount)
            )
            operation_id = await conn.fetchval(query, *params)

            query = """
            INSERT INTO operation_history
                (operation_id)
            VALUES ($1);
            """

            params = (operation_id, )

            await conn.execute(query, *params)

    return operation_id


async def send_to_processing(pool, operation_id):
    """
        Move draft operation to processing status.
        This function emulates processing outside of payments service
    """
    # TODO: timeout to settings

    query = """
        INSERT INTO operation_history
            (operation_id, status)
        VALUES ($1, $2) RETURNING id;
    """
    # TODO: move int cast outside of function
    params = (int(operation_id), OperationStatusEnum.PROCESSING)

    async with pool.acquire(timeout=10) as conn:
        result = await conn.fetchval(query, *params)

    return result
