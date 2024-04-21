import pytest
from sqlalchemy.exc import ProgrammingError

from src.di.container import UnitOfWork
import sqlalchemy as sa

from src.infra.db.postgresql.public import book


async def test_migrations(migrations):
    assert True


async def test_container_pool(migrations, transaction):
    uow: UnitOfWork
    async with transaction as uow:
        await uow.connection.execute(sa.select(book).limit(1))


async def test_container_pool_migrations_not_applied(transaction):
    uow: UnitOfWork
    async with transaction as uow:
        with pytest.raises(ProgrammingError):
            await uow.connection.execute(sa.select(book).limit(1))
