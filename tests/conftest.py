# pylint: disable=redefined-outer-name,C0413
import pytest
from alembic.command import downgrade as alembic_downgrade
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from fastapi.testclient import TestClient

from src.app import app
from src.di.container import init_container


@pytest.fixture
async def migrations(event_loop, container):  # pylint: disable=unused-argument
    """fixture for migrations"""

    config = AlembicConfig('alembic.ini')
    alembic_upgrade(config, 'head')

    yield

    alembic_downgrade(config, 'base')


@pytest.fixture
async def application(migrations, container):  # pylint: disable=W0613
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


@pytest.fixture
async def uowm(container):
    uow = await container.uow()
    yield uow
