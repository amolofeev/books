import asyncpg
from dependency_injector import containers, providers
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine


class AsyncpgSqlaConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ASYNCPG_SQLA_", env_file=".env", extra="ignore")
    CONNECTION_STRING: str
    CONNECTION_TIMEOUT: int = 20
    MIN_POOL_SIZE: int = 1
    MAX_POOL_SIZE: int = 5


config = AsyncpgSqlaConfig()


async def _init_pg_pool():
    pool = await asyncpg.create_pool(
        dsn=config.CONNECTION_STRING,
        timeout=config.CONNECTION_TIMEOUT,
        min_size=config.MIN_POOL_SIZE,
        max_size=config.MAX_POOL_SIZE,
    )
    yield pool

    await pool.close()


class AsyncpgSQLAContainer(containers.DeclarativeContainer):
    pool = providers.Resource(
        _init_pg_pool,
    )
