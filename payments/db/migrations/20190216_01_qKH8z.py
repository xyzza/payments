"""
Create initial db schema
"""

from yoyo import step

__depends__ = {'__init__'}

steps = [
    step("""
            CREATE TYPE CURRENCY AS ENUM ('USD', 'EUR', 'CAD', 'CNY');
            CREATE TYPE STATUS AS ENUM ('DRAFT', 'PROCESSING', 'ACCEPTED', 'FAILED');
            
            CREATE TABLE account (
                -- user account id
                id SERIAL PRIMARY KEY,
                -- user first name
                first_name VARCHAR (200) NOT NULL,
                -- user last name
                last_name VARCHAR (200) NOT NULL,
                -- user country name
                country VARCHAR (300) NOT NULL,
                -- user wallet currency
                currency CURRENCY DEFAULT 'USD' NOT NULL,
                -- user wallet balance
                balance DECIMAL (16,2) DEFAULT 0.00,
                -- unique user name
                CONSTRAINT unq_name UNIQUE(first_name,last_name)
            );
            
            CREATE TABLE operation (
                -- operation id
                id SERIAL PRIMARY KEY,
                -- operation sender FK
                sender_id INTEGER REFERENCES account(id) NOT NULL,
                -- operation recipient FK
                recipient_id INTEGER REFERENCES account(id) NOT NULL,
                -- operation volume
                amount DECIMAL (16,2) NOT NULL,
                -- operation timestamp
                timestamp TIMESTAMP DEFAULT current_timestamp NOT NULL
            );
            
            CREATE TABLE operation_history (
                -- history id
                id SERIAL PRIMARY KEY,
                -- operation FK
                operation_id INTEGER REFERENCES operation(id) NOT NULL,
                -- operation status
                status STATUS DEFAULT 'DRAFT' NOT NULL,
                -- timestamp
                timestamp TIMESTAMP DEFAULT current_timestamp NOT NULL,
                -- unique status in one operation
                CONSTRAINT unq_operation_id_status UNIQUE(operation_id,status)
            );
        """,
        """
            DROP TABLE operation_history;
            DROP TABLE operation;
            DROP TABLE account;
        
            DROP TYPE STATUS;
            DROP TYPE CURRENCY;
        """)
]

# тип операции не нужен, потому что мы не можем сделать операцию по списанию с чужого аккаунта себе на счет,
# мы можем только зачислить со своего аккаунта на чужой счет
# -- operation type could be -1, that's mean credit, or 1, that's mean debit
#                 type SMALLINT NOT NULL CHECK (type = -1 or type = 1)
