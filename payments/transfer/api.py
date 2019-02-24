from decimal import Decimal

import asyncpg

from payments import settings
from payments.account import AccountDoesNotExists
from payments.account import account_balance
from payments.account import account_balances_pair
from payments.operation import OperationTypeEnum
from payments.operation import create_operation
from payments.operation import init_operation_draft


async def credit_funds(pool, account_id: int, amount: Decimal) -> int:

    async with pool.acquire(timeout=settings.DB_TIMEOUT) as conn:

        try:

            async with conn.transaction():

                balance = await account_balance(
                    pool,
                    account_id
                )

                return await _create_operation(
                    conn,
                    account_id,
                    account_id,
                    amount,
                    OperationTypeEnum.CREDIT,
                    balance,
                    balance
                )

        except asyncpg.exceptions.ForeignKeyViolationError:
                raise AccountDoesNotExists()


async def transfer_funds(
        pool,
        sender_account_id: int,
        recipient_account_id: int,
        amount: Decimal) -> int:

    async with pool.acquire(timeout=settings.DB_TIMEOUT) as conn:

        try:

            async with conn.transaction():

                sender_balance, recipient_balance = await account_balances_pair(
                    pool,
                    sender_account_id,
                    recipient_account_id
                )

                return await _create_operation(
                    conn,
                    sender_account_id,
                    recipient_account_id,
                    amount,
                    OperationTypeEnum.TRANSFER,
                    sender_balance,
                    recipient_balance
                )

        except asyncpg.exceptions.ForeignKeyViolationError:
            raise AccountDoesNotExists()


async def _create_operation(
        conn,
        sender,
        recipient,
        amount,
        o_type,
        sender_balance,
        recipient_balance):

    operation_id = await conn.fetchval(
            create_operation,
            sender,
            recipient,
            amount,
            o_type
        )

    await conn.execute(
        init_operation_draft,
        operation_id,
        sender_balance,
        recipient_balance
    )

    return operation_id
