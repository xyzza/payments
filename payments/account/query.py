create_account = """
INSERT INTO account
    (first_name, last_name, country, currency)
VALUES ($1, $2, $3, $4) RETURNING id;
"""

account_balance = """
SELECT balance FROM account WHERE id = $1;
"""

account_balances_pair = """
SELECT balance FROM account WHERE id = $1
UNION ALL 
SELECT balance FROM account WHERE id = $2;
"""
