import asyncpg

from payments import settings
from payments.converter import convert_currency
from payments.operation import OperationDoesNotExists
from payments.operation import OperationInconsistent
from payments.operation import OperationStatusEnum
from payments.operation import OperationTypeEnum
from payments.operation import operation_to_processing
from payments.operation import select_operation_info
from payments.operation import update_operation_status

from .query import decrease_balance
from .query import increase_balance
from .query import select_and_lock_accounts


async def process_credit_operation(pool, operation_id: int) -> OperationStatusEnum:

    async with pool.acquire(timeout=settings.DB_TIMEOUT) as conn:

        try:

            async with conn.transaction():

                try:
                    _, recipient_id, amount = await conn.fetchrow(
                        select_operation_info,
                        OperationStatusEnum.PROCESSING,
                        operation_id,
                        OperationTypeEnum.CREDIT
                    )
                except TypeError:
                    raise OperationDoesNotExists()

                await conn.execute(increase_balance, recipient_id, amount)

                status = await conn.fetchval(
                    update_operation_status,
                    operation_id,
                    OperationStatusEnum.ACCEPTED,
                    OperationStatusEnum.COUNT[OperationStatusEnum.ACCEPTED]
                )

                return status

        except asyncpg.exceptions.UniqueViolationError:
            raise OperationInconsistent()


async def process_transfer_operation(pool, operation_id: int) -> OperationStatusEnum:

    async with pool.acquire(timeout=settings.DB_TIMEOUT) as conn:

        try:

            async with conn.transaction():

                try:
                    sender_id, recipient_id, amount = await conn.fetchrow(
                        select_operation_info,
                        OperationStatusEnum.PROCESSING,
                        operation_id,
                        OperationTypeEnum.TRANSFER
                    )
                except TypeError:
                    raise OperationDoesNotExists()

                sender_data, recipient_data = await conn.fetch(
                    select_and_lock_accounts,
                    sender_id,
                    recipient_id
                )

                sender_balance, sender_currency = sender_data
                recipient_balance, recipient_currency = recipient_data

                if sender_balance >= amount:
                    # transfer
                    await conn.execute(decrease_balance, sender_id, amount)

                    credit = convert_currency(amount, sender_currency, recipient_currency)
                    await conn.execute(increase_balance, recipient_id, credit)

                    resulting_status = OperationStatusEnum.ACCEPTED

                else:
                    # not enough funds for withdrawal
                    resulting_status = OperationStatusEnum.FAILED

                status = await conn.fetchval(
                    update_operation_status,
                    operation_id,
                    resulting_status,
                    OperationStatusEnum.COUNT[resulting_status]
                )

                return status

        except asyncpg.exceptions.UniqueViolationError:
            raise OperationInconsistent()


async def send_to_processing(pool, operation_id: int) -> int:
    """
        Move draft operation to processing status.
        This function emulates processing outside of payments service
    """

    async with pool.acquire(timeout=settings.DB_TIMEOUT) as conn:

        try:
            result = await conn.fetchval(
                operation_to_processing,
                operation_id,
                OperationStatusEnum.PROCESSING,
                OperationStatusEnum.COUNT[OperationStatusEnum.PROCESSING]
            )
        except asyncpg.exceptions.ForeignKeyViolationError:
            raise OperationDoesNotExists()

    return result
