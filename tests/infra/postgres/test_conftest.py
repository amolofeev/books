import pytest
import sqlalchemy as sa
from sqlalchemy.exc import ProgrammingError

from src.di.container import UnitOfWork
from src.infra.db.postgresql.public import book


async def test_migrations(pg_container):
    assert True


async def test_container_pool(pg_container, uow: UnitOfWork):
    async with uow:
        await uow.connection.execute(sa.select(book).limit(1))


async def test_container_pool_migrations_not_applied(uow: UnitOfWork):
    async with uow:
        with pytest.raises(ProgrammingError):
            await uow.connection.execute(sa.select(book).limit(1))
