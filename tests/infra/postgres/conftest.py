import pytest
from alembic.command import downgrade as alembic_downgrade
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig


@pytest.fixture
async def migrations(event_loop):  # pylint: disable=unused-argument
    """fixture for migrations"""

    config = AlembicConfig('alembic.ini')
    alembic_upgrade(config, 'head')
    yield
    alembic_downgrade(config, 'base')
