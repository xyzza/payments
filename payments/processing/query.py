select_and_lock_accounts = """
SELECT balance, currency FROM account WHERE id in ($1, $2) ORDER BY ID FOR UPDATE;
"""

decrease_balance = """
WITH current_balance AS (SELECT balance FROM account WHERE id = $1)
UPDATE account 
    SET balance = (SELECT current_balance.balance - $2 FROM current_balance) 
    WHERE id = $1 RETURNING balance;
"""

increase_balance = """
WITH current_balance AS (SELECT balance FROM account WHERE id = $1)
UPDATE account 
    SET balance = (SELECT current_balance.balance + $2 FROM current_balance) 
    WHERE id = $1 RETURNING balance;
"""
