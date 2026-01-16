import pytest

from src.di.container import UnitOfWork
from src.domain.dto.book import BookDTO
from src.domain.factory.book import BookDTOFactory


async def test_create_book_dao(uow: UnitOfWork) -> None:
    book: BookDTO = BookDTOFactory.create()
    async with uow.connection() as conn, conn.transaction():
        await uow.book._dao.create(book)
        new_book = await uow.book._dao.get_by_id(book.id)
    assert book == new_book


@pytest.mark.skip("TODO:")
async def test_recreate_book_dao(uow: UnitOfWork) -> None: ...


@pytest.mark.skip("TODO:")
async def test_update_book_dao(uow: UnitOfWork) -> None: ...


@pytest.mark.skip("TODO:")
async def test_delete_book_dao(uow: UnitOfWork) -> None: ...


@pytest.mark.skip("TODO:")
async def test_get_list_book_dao(uow: UnitOfWork) -> None: ...


@pytest.mark.skip("TODO:")
async def test_get_list_by_author_dao(uow: UnitOfWork) -> None: ...


@pytest.mark.skip("TODO:")
async def test_get_list_by_category_dao(uow: UnitOfWork) -> None: ...
