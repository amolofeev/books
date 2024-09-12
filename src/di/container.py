# pylint: disable=c-extension-no-member
import dataclasses

# import os
# import pathlib
from typing import Any

from dependency_injector import containers, providers

from src.di.file_storage import FileStorageContainer
from src.di.repository.author import AuthorRepositoryContainer
from src.di.repository.book import BookRepositoryContainer
from src.di.repository.category import CategoryRepositoryContainer
from src.di.repository.m2m_author_book import M2MAuthorBookRepositoryContainer
from src.di.repository.m2m_category_book import M2MCategoryBookRepositoryContainer
from src.di.sqlalchemy_asyncpg import AsyncpgSQLAContainer
from src.domain.interface.author import IAuthorDAO
from src.domain.interface.book import IBookDAO
from src.domain.interface.category import ICategoryDAO
from src.domain.interface.m2m_author_book import IM2MAuthorBookDAO
from src.domain.interface.m2m_category_book import IM2MCategoryBookDAO
from src.domain.interface.storage import IStorageDAO
from src.vars import PGConnection

# from jinja2 import Environment, FileSystemLoader, select_autoescape


@dataclasses.dataclass
class UnitOfWork:
    pg_connection_pool: Any
    book: IBookDAO
    author: IAuthorDAO
    category: ICategoryDAO
    m2m_author_book: IM2MAuthorBookDAO
    m2m_category_book: IM2MCategoryBookDAO
    storage: IStorageDAO

    @property
    def connection(self):
        return PGConnection.get()

    async def __aenter__(self) -> None:
        _connection = await self.pg_connection_pool.connect()
        transaction = await _connection.begin()
        PGConnection.set(_connection)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        _connection = PGConnection.get()
        if exc_type is None:
            await _connection.commit()
        else:
            await _connection.rollback()
        await _connection.close()


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.domain",
        ],
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

    _book_repository = providers.Container(BookRepositoryContainer)
    _author_repository = providers.Container(AuthorRepositoryContainer)
    _category_repository = providers.Container(CategoryRepositoryContainer)
    _m2m_author_book_repository = providers.Container(M2MAuthorBookRepositoryContainer)
    _m2m_category_book_repository = providers.Container(M2MCategoryBookRepositoryContainer)
    _file_storage = providers.Container(FileStorageContainer)

    uow = providers.Factory(
        UnitOfWork,
        pg_connection_pool=_pg_connection_pool.pool,
        book=_book_repository.repository,
        author=_author_repository.repository,
        category=_category_repository.repository,
        m2m_author_book=_m2m_author_book_repository.repository,
        m2m_category_book=_m2m_category_book_repository.repository,
        storage=_file_storage.repository,
    )


async def init_container(**kwargs) -> Container:
    defaults = {
        **kwargs,
    }
    container = Container(**defaults)
    await container.init_resources()
    return container
