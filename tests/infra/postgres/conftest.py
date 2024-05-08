import pytest
from alembic.command import downgrade as alembic_downgrade
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig

from src.di.container import init_container


@pytest.fixture
async def pg_container(event_loop):  # pylint: disable=unused-argument
    """fixture for migrations"""

    config = AlembicConfig('alembic.ini')
    alembic_upgrade(config, 'head')

    container = await init_container()
    yield container
    await container.shutdown_resources()

    alembic_downgrade(config, 'base')
