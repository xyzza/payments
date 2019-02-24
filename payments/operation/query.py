create_operation = """
INSERT INTO operation
    (sender_id, recipient_id, amount, type)
VALUES ($1, $2, $3, $4) RETURNING id;
"""

init_operation_draft = """
INSERT INTO operation_history
    (operation_id, sender_balance, recipient_balance)
VALUES ($1, $2, $3);
"""

operation_to_processing = """
INSERT INTO operation_history
    (operation_id, status, status_count, sender_balance, recipient_balance)
VALUES ($1, $2, $3, $4, $5) RETURNING id;
"""

select_operation_info = """
SELECT sender_id, recipient_id, amount FROM operation o
INNER JOIN operation_history oh
    ON o.id = oh.operation_id
    AND oh.status=$1
    AND o.id = $2
    AND o.type = $3;
"""

update_operation_status = """
INSERT INTO operation_history
    (operation_id, status, status_count, sender_balance, recipient_balance)
VALUES ($1, $2, $3, $4, $5) RETURNING status;
"""

select_balances_pair_from_history = """
SELECT sender_balance, recipient_balance FROM operation_history
    WHERE operation_id = $1
    AND status = $2;
"""
