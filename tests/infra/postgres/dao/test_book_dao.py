import pytest

from src.di.container import UnitOfWork
from src.domain.dto.book import BookDTO
from src.domain.factory.book import BookDTOFactory
from src.vars import PGConnection


async def test_create_book_dao(pg_container):
    uow: UnitOfWork = await pg_container.uow()
    book: BookDTO = BookDTOFactory.create()
    async with uow.pg_connection_pool.begin() as conn:
        PGConnection.set(conn)
        await uow.book._dao.create(book)
        new_book = await uow.book._dao.get_by_id(book.id)
    assert book == new_book


@pytest.mark.skip('TODO:')
async def test_recreate_book_dao(pg_container):
    ...


@pytest.mark.skip('TODO:')
async def test_update_book_dao(pg_container):
    ...


@pytest.mark.skip('TODO:')
async def test_delete_book_dao(pg_container):
    ...


@pytest.mark.skip('TODO:')
async def test_get_list_book_dao(pg_container):
    ...


@pytest.mark.skip('TODO:')
async def test_get_list_by_author_dao(pg_container):
    ...


@pytest.mark.skip('TODO:')
async def test_get_list_by_category_dao(pg_container):
    ...
