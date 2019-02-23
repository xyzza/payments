from envparse import Env

env = Env()


DB_DSN = env.str(
    'DB_DSN',
    default='postgresql://postgres:postgres@localhost:5432/payments'
)

DB_POOL_SIZE = env.int('DB_POOL_SIZE', default=10)
DB_TIMEOUT = env.int('DB_TIMEOUT', default=10)
