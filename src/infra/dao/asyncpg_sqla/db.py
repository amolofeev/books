from src.vars import PGConnection
from sqlalchemy.dialects.postgresql.asyncpg import dialect


def _compile(stmt, dialect=dialect()):
    c = stmt.compile(dialect=dialect)
    return c.string, *c.params.values()


async def fetch(stmt):
    conn = PGConnection.get()
    return await conn.fetch(*_compile(stmt))


async def fetchval(stmt):
    conn = PGConnection.get()
    return await conn.fetchval(*_compile(stmt))


async def fetchrow(stmt):
    conn = PGConnection.get()
    return await conn.fetchrow(*_compile(stmt))


async def execute(stmt):
    conn = PGConnection.get()
    # prevent autocommit
    assert conn.is_in_transaction()
    return await conn.execute(*_compile(stmt))


# async def executemany(stmt):
#     conn = PGConnection.get()
#     assert conn.is_in_transaction()
#     return await conn.executemany(*_compile(stmt))
