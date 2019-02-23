create_operation = """
INSERT INTO operation
    (sender_id, recipient_id, amount, type)
VALUES ($1, $2, $3, $4) RETURNING id;
"""

init_operation_draft = """
INSERT INTO operation_history
    (operation_id)
VALUES ($1);
"""

operation_to_processing = """
INSERT INTO operation_history
    (operation_id, status, status_count)
VALUES ($1, $2, $3) RETURNING id;
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
    (operation_id, status, status_count)
VALUES ($1, $2, $3) RETURNING status;
"""
