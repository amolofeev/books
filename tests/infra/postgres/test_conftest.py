# ruff: noqa: ARG001, S101

import sqlalchemy as sa

from src.di.container import UnitOfWork
from src.infra.db.postgresql.public import book


async def test_migrations(migrations) -> None:
    assert True


async def test_container_pool(uow: UnitOfWork) -> None:
    async with uow.connection() as conn:
        await conn.fetchrow(sa.select(book).limit(1))
