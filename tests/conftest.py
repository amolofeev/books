# pylint: disable=redefined-outer-name,C0413
import pytest
from alembic.command import downgrade as alembic_downgrade
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncEngine

from src.app import app
from src.di.container import init_container


@pytest.fixture
async def pg_engine(event_loop, container):  # pylint: disable=unused-argument
    """fixture for migrations"""

    config = AlembicConfig('alembic.ini')
    alembic_upgrade(config, 'head')

    yield container._connection_pool

    alembic_downgrade(config, 'base')


@pytest.fixture
async def db_connection(pg_engine: AsyncEngine):
    """fixture for connection"""
    async with pg_engine.begin() as conn:
        yield conn


@pytest.fixture
async def application(pg_engine, container):  # pylint: disable=W0613
    """override dependencies"""
    yield app


@pytest.fixture
async def client(application):
    """Test http client"""
    yield TestClient(application)


@pytest.fixture
async def container():
    container = await init_container()
    yield container
    await container.shutdown_resources()
