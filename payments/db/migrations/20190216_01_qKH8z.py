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
                balance DECIMAL (16,2) DEFAULT 0.00 NOT NULL,

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
                timestamp TIMESTAMP DEFAULT current_timestamp NOT NULL,
                -- operation type 1 is for credit 2 is for transfer
                type SMALLINT NOT NULL CHECK (
                    (type=1 and sender_id = recipient_id) or (type=2 and sender_id != recipient_id)
                )
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
                -- counts number of statuses
                status_count SMALLINT DEFAULT 1 NOT NULL CHECK (status_count > 0 and status_count < 4),
                -- sender_balance
                sender_balance DECIMAL (16,2) NOT NULL,
                -- recipient_balance
                recipient_balance DECIMAL (16,2) NOT NULL,
                
                -- unique operation_id and status 
                CONSTRAINT unq_operation_id_status UNIQUE(operation_id, status),
                -- unique operation_id and status_count
                CONSTRAINT unq_operation_id_status_count UNIQUE(operation_id, status_count)
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
