from urllib.parse import urlparse

import psycopg2
import pytest
from alembic.command import downgrade as alembic_downgrade
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from src.di.container import Container, UnitOfWork, init_container
from src.di.sqlalchemy_asyncpg import config as asyncpg_config


@pytest.fixture(scope='session', autouse=True)
async def migrations_config(worker_id):

    parsed = urlparse(asyncpg_config.DSN)
    new_database_name = f'{parsed.path}_{worker_id}'
    parsed = parsed._replace(path=new_database_name)

    connection = psycopg2.connect(asyncpg_config.DSN)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    try:
        cursor.execute(f'CREATE DATABASE {new_database_name[1:]};')
    except BaseException:
        pass
    finally:
        cursor.close()
        connection.close()
    asyncpg_config.DSN = parsed.geturl()
    config = AlembicConfig('alembic.ini')
    config.set_main_option('sqlalchemy.url', parsed.geturl())
    return config


@pytest.fixture
async def migrations(migrations_config):  # pylint: disable=unused-argument
    """Fixture for migrations."""

    alembic_downgrade(migrations_config, 'base')
    alembic_upgrade(migrations_config, "head")

    yield

    alembic_downgrade(migrations_config, "base")


@pytest.fixture
async def container(migrations) -> Container:
    container = await init_container()
    yield container
    await container.shutdown_resources()


@pytest.fixture
async def uow(container: Container) -> UnitOfWork:
    return await container.uow()