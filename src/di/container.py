# pylint: disable=c-extension-no-member
import dataclasses
import os
import pathlib
from contextlib import asynccontextmanager
from typing import Any

from dependency_injector import containers, providers
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy.ext.asyncio import create_async_engine

from src.domain.interface.books import IBookDAO
from src.domain.interface.tags import ITagsDAO
from src.infra.dao.postgresql.books import BooksDAO
from src.infra.dao.postgresql.m2m_tag_book import M2MTagBookDAO
from src.infra.dao.postgresql.tags import TagsDAO
from src.infra.repository.books import BookRepository
from src.infra.repository.m2m_tag_book import M2MTagBookRepository
from src.infra.repository.tags import TagsRepository
from src.settings import settings
from src.vars import PGConnection


async def init_pg_pool():
    pool = create_async_engine(
        url=settings.db.CONNECTION_STRING,
        pool_timeout=settings.db.CONNECTION_TIMEOUT,
        pool_size=settings.db.MIN_POOL_SIZE,
    )
    yield pool

    await pool.dispose(True)


@asynccontextmanager
async def uow_manager(**kwargs):
    @dataclasses.dataclass
    class UnitOfWork:
        connection_pool: Any
        books: IBookDAO
        tags: ITagsDAO
        m2m: M2MTagBookDAO

        @property
        def connection(self):
            return PGConnection.get()

    uow = UnitOfWork(**kwargs)
    async with uow.connection_pool.begin() as conn:
        PGConnection.set(conn)
        yield uow


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.domain",
            "src.interface",
        ]
    )
    render = providers.Singleton(
        Environment,
        loader=FileSystemLoader(
            pathlib.Path(os.getcwd())/'src/interface/rest/fastapi/templates'
        ),
        autoescape=select_autoescape()
    )
    _connection_pool = providers.Resource(
        init_pg_pool,
    )
    _books_dao = providers.Singleton(BooksDAO)
    _books_repo = providers.Singleton(
        BookRepository,
        dao=_books_dao,
    )

    _tags_dao = providers.Singleton(TagsDAO)
    _tags_repo = providers.Singleton(
        TagsRepository,
        dao=_tags_dao,
    )

    _m2m_dao = providers.Singleton(M2MTagBookDAO)
    _m2m_repo = providers.Singleton(
        M2MTagBookRepository,
        dao=_m2m_dao,
    )

    uow = providers.Factory(
        uow_manager,
        books=_books_repo,
        tags=_tags_repo,
        m2m=_m2m_repo,
        connection_pool=_connection_pool,
    )


async def init_container(**kwargs) -> containers.DeclarativeContainer:
    defaults = {
        **kwargs,
    }
    container = Container(**defaults)
    await container.init_resources()
    return container
