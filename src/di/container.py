# pylint: disable=c-extension-no-member
import dataclasses
# import os
# import pathlib
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from dependency_injector import containers, providers

from src.di.sqlalchemy_asyncpg import AsyncpgSQLAContainer
from src.vars import PGConnection


# from jinja2 import Environment, FileSystemLoader, select_autoescape



@dataclasses.dataclass
class UnitOfWork:
    pg_connection_pool: Any

    @property
    def connection(self):
        return PGConnection.get()


@asynccontextmanager
async def _transaction_manager(**kwargs) -> AsyncGenerator[UnitOfWork, None]:
    uow = UnitOfWork(**kwargs)
    async with uow.pg_connection_pool.begin() as conn:
        PGConnection.set(conn)
        yield uow


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.domain",
            "src.interface",
        ]
    )
    # render = providers.Singleton(
    #     Environment,
    #     loader=FileSystemLoader(
    #         pathlib.Path(os.getcwd())/'src/interface/rest/litestar/templates'
    #     ),
    #     autoescape=select_autoescape()
    # )
    _pg_connection_pool = providers.Container(
        AsyncpgSQLAContainer,
    )

    transaction = providers.Factory(
        _transaction_manager,
        pg_connection_pool=_pg_connection_pool.pool,
    )


async def init_container(**kwargs) -> containers.DeclarativeContainer:
    defaults = {
        **kwargs,
    }
    container = Container(**defaults)
    await container.init_resources()
    return container
