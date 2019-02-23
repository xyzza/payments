from payments import settings


async def billing_report(pool, first_name, last_name, begin=None, end=None):

    async with pool.acquire(timeout=settings.DB_TIMEOUT) as conn:

        params = [first_name, last_name]
        extra = ';'

        if begin and end:
            extra = f'AND oh.timestamp between({begin}, {end}){extra}'
            params.extend([begin, end])
        elif begin:
            extra = f'AND oh.timestamp >= {begin}{extra}'
            params.append(begin)
        elif end:
            extra = f'AND oh.timestamp <= {begin}{extra}'
            params.append(end)

        query = f"""
        WITH report_user as (SELECT id FROM account WHERE first_name=$1 AND last_name=$2)
        SELECT 
            (o.sender_id = o.recipient_id) as op_type, 
            COALESCE(to_char(oh.timestamp, 'DD-MM-YYYY HH24:MI:SS'), '') as timestamp, 
            a.first_name, 
            a.last_name, 
            a.balance, 
            o.id, 
            o.amount, 
            oh.status  
        FROM operation_history oh
        INNER JOIN operation o 
            ON oh.operation_id = o.id
        INNER JOIN account a 
            ON o.recipient_id = a.id
        WHERE o.sender_id = (SELECT id FROM report_user) 
            OR o.recipient_id = (SELECT id FROM report_user)
        {extra}
        """

        rows = await conn.fetch(query, *params)

        return rows
