create_account = """
INSERT INTO account
    (first_name, last_name, country, currency)
VALUES ($1, $2, $3, $4) RETURNING id;
"""

account_balance = """
SELECT balance FROM account WHERE id = $1
"""
