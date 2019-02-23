from decimal import Decimal

import asyncpg

from payments import settings
from payments.account import AccountDoesNotExists
from payments.operation import OperationTypeEnum
from payments.operation import create_operation
from payments.operation import init_operation_draft


async def credit_funds(pool, account_id: int, amount: Decimal) -> int:

    async with pool.acquire(timeout=settings.DB_TIMEOUT) as conn:
        # TODO: duplicated code
        try:

            async with conn.transaction():
                return await _create_operation(
                    conn,
                    account_id,
                    account_id,
                    amount,
                    OperationTypeEnum.CREDIT
                )

        except asyncpg.exceptions.ForeignKeyViolationError:
                raise AccountDoesNotExists()


async def transfer_funds(
        pool,
        sender_account_id: int,
        recipient_account_id: int,
        amount: Decimal) -> int:

    async with pool.acquire(timeout=settings.DB_TIMEOUT) as conn:
        # TODO: duplicated code
        try:

            async with conn.transaction():

                return await _create_operation(
                    conn,
                    sender_account_id,
                    recipient_account_id,
                    amount,
                    OperationTypeEnum.TRANSFER
                )

        except asyncpg.exceptions.ForeignKeyViolationError:
            raise AccountDoesNotExists()


async def _create_operation(conn, sender, recipient, amount, o_type):

    operation_id = await conn.fetchval(
            create_operation,
            sender,
            recipient,
            amount,
            o_type
        )

    await conn.execute(init_operation_draft, operation_id)

    return operation_id
