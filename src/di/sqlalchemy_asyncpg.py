import asyncpg
from dependency_injector import containers, providers
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.settings import settings


class AsyncpgSqlaConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ASYNCPG_", env_file=".env", extra="ignore")
    DSN: str
    CONNECTION_TIMEOUT: float = 0.200  # 200ms
    MIN_POOL_SIZE: int = 1
    MAX_POOL_SIZE: int = 5
    POOL_TIMEOUT: float = 0.200  # 200ms


config = AsyncpgSqlaConfig()


async def _init_pg_pool():
    pool = await asyncpg.create_pool(
        # connection settings
        dsn=config.DSN,
        timeout=config.CONNECTION_TIMEOUT,
        # pool settings
        min_size=config.MIN_POOL_SIZE,
        max_size=config.MAX_POOL_SIZE,
        # connection params
        server_settings={
            "application_name": settings.app.NAME,
            "timezone": "utc",
        },
    )
    yield pool

    await pool.close()


class AsyncpgSQLAContainer(containers.DeclarativeContainer):
    pool = providers.Resource(
        _init_pg_pool,
    )
