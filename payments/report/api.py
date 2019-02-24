from payments import settings
from payments.account import AccountDoesNotExistsError
from .query import find_report_account
from .query import find_participants
from .query import fetch_report
from .query import between_condition
from .query import begin_condition
from .query import end_condition


async def billing_report(pool, first_name, last_name, begin=None, end=None):

    async with pool.acquire(timeout=settings.DB_TIMEOUT) as conn:

        account_id = await conn.fetchval(find_report_account, first_name, last_name)

        if account_id is None:
            raise AccountDoesNotExistsError()

        participants = await conn.fetch(find_participants, account_id)

        if not participants:
            return []

        participants = [
            (f'${p[0]+1}', p[1][0]) for p in enumerate(participants)
        ]
        indexes, participants = zip(*participants)
        participants = list(participants)

        params = ','.join(indexes)

        if begin and end:
            participants.extend([begin, end])
            _where = between_condition.format(
                begin=f'${ len(participants)-1}',
                end=f'${len(participants)}'
            )
        elif begin:
            participants.append(begin)
            _where = begin_condition.format(begin=f'${len(participants)}')
        elif end:
            participants.append(end)
            _where = end_condition.format(end=f'${len(participants)}')
        else:
            _where = ''

        query = fetch_report.format(
            where_condition=_where,
            params=params
        )

        report_rows = await conn.fetch(query, *participants)

        return report_rows
