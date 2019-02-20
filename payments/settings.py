from envparse import Env

env = Env()


DB_DSN = env.str(
    'DB_DSN',
    default='postgresql://postgres:postgres@localhost:5432/payments'
)

DB_POOL_SIZE = 10
