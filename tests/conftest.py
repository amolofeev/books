# pylint: disable=redefined-outer-name,C0413
from typing import AsyncGenerator

import pytest
from alembic.command import downgrade as alembic_downgrade
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig

from src.di.container import UnitOfWork, init_container


@pytest.fixture
async def pg_container(event_loop, container):  # pylint: disable=unused-argument
    """fixture for migrations"""

    config = AlembicConfig('alembic.ini')
    alembic_upgrade(config, 'head')

    container = await init_container()

    yield container

    await container.shutdown_resources()

    alembic_downgrade(config, 'base')


@pytest.fixture
async def container():
    container = await init_container()
    yield container
    await container.shutdown_resources()


@pytest.fixture
async def uow(container) -> AsyncGenerator[UnitOfWork, None]:
    uow = await container.uow()
    yield uow
