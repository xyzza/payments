from decimal import Decimal

from payments.converter import convert_currency
from payments.transfer import OperationStatusEnum


async def process_credit_operation(pool, operation_id: int) -> OperationStatusEnum:

    async with pool.acquire(timeout=10) as conn:

        async with conn.transaction():
            # TODO: check that accepted / failed status doesn't exists
            query = """
            SELECT sender_id, recipient_id, volume FROM operation o
            INNER JOIN operation_history oh
                ON o.id = oh.operation_id
                AND oh.status=$1
                AND o.id = $2;
            """

            params = (OperationStatusEnum.PROCESSING, int(operation_id))
            # TODO: check sender_id == recipient_id
            _, recipient_id, amount = await conn.fetchrow(query, *params)

            query = """
            WITH current_balance AS (SELECT balance FROM account WHERE id = $1 FOR UPDATE)
            UPDATE account 
                SET balance = (SELECT current_balance.balance + $2 FROM current_balance) 
                WHERE id = $1;
            """

            params = (int(recipient_id), Decimal(amount))

            await conn.execute(query, *params)

            query = """
            INSERT INTO operation_history
                (operation_id, status)
            VALUES ($1, $2) RETURNING status;
            """

            params = (int(operation_id), OperationStatusEnum.ACCEPTED)

            status = await conn.fetchval(query, *params)

            return status


async def process_transfer_operation(pool, operation_id: int) -> OperationStatusEnum:

    async with pool.acquire(timeout=10) as conn:

        async with conn.transaction():
            # TODO: check that accepted / failed status doesn't exists
            query = """
            SELECT sender_id, recipient_id, volume, currency FROM operation o
            INNER JOIN operation_history oh
                ON o.id = oh.operation_id
                AND oh.status=$1
                AND o.id = $2;
            """

            params = (OperationStatusEnum.PROCESSING, int(operation_id))
            # TODO: check sender_id == recipient_id
            sender_id, recipient_id, amount, currency = await conn.fetchrow(
                query,
                *params
            )

            query = """
            SELECT balance, currency FROM account WHERE id in ($1, $2) ORDER BY ID FOR UPDATE;
            """

            params = (int(sender_id), int(recipient_id))

            sender_data, recipient_data = await conn.fetch(query, *params)

            sender_balance, sender_currency = sender_data
            recipient_balance, recipient_currency = recipient_data

            debit = convert_currency(amount, currency, sender_currency)

            if debit > sender_balance:
                # not enough funds for withdrawal
                resulting_status = OperationStatusEnum.FAILED

            else:
                # transfer

                query = """
                WITH current_balance AS (SELECT balance FROM account WHERE id = $1)
                UPDATE account 
                    SET balance = (SELECT current_balance.balance - $2 FROM current_balance) 
                    WHERE id = $1;
                """

                params = (int(sender_id), debit)

                await conn.execute(query, *params)

                credit = convert_currency(amount, currency, recipient_currency)

                query = """
                WITH current_balance AS (SELECT balance FROM account WHERE id = $1)
                UPDATE account 
                    SET balance = (SELECT current_balance.balance + $2 FROM current_balance) 
                    WHERE id = $1;
                """

                params = (int(recipient_id), credit)

                await conn.execute(query, *params)

                resulting_status = OperationStatusEnum.ACCEPTED

            query = """
            INSERT INTO operation_history
                (operation_id, status)
            VALUES ($1, $2) RETURNING status;
            """

            params = (int(operation_id), resulting_status)

            status = await conn.fetchval(query, *params)

            return status
