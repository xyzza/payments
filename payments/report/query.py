find_report_account = """SELECT id from account WHERE first_name=$1 and last_name=$2;"""

find_participants = """ 
select recipient_id from operation where sender_id = $1
union
select sender_id from operation where recipient_id = $1;
"""

fetch_report = """
WITH accounts AS (
    SELECT CONCAT(first_name, ' ', last_name) AS username, id
    FROM account where id in ({params}))
SELECT
        oh.timestamp,
        sender_id,
        a.username as from_user,
        (CASE
                WHEN op.type = 1
                    THEN 'credit->'

                ELSE '<-transfer->'
        END) as op_type,
        op.amount,
        recipient_id,
        a2.username as to_user,
        oh.status,
        oh.sender_balance,
        oh.recipient_balance
FROM operation op
INNER JOIN operation_history oh on op.id = oh.operation_id
INNER JOIN accounts a on op.sender_id = a.id
INNER JOIN accounts a2 on op.recipient_id = a2.id
{where_condition}
ORDER BY oh.timestamp;
"""

between_condition = """WHERE oh.timestamp between {begin} AND {end}"""

begin_condition = """WHERE oh.timestamp >= {begin}"""

end_condition = """WHERE oh.timestamp <= {end}"""
