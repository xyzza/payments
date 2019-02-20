import asyncpg


async def create_pool(dsn, size):
    return await asyncpg.create_pool(dsn=dsn, max_size=size)
