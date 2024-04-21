import pytest
from sqlalchemy.exc import NoResultFound

from src.domain.dto.books import BookDTO, CreateBookFactory


async def test_create_book_repo(uowm, migrations):
    book = CreateBookFactory.create()
    async with uowm as uow:
        new_book = await uow.books.create_book(book)
        assert isinstance(new_book, BookDTO)
        assert new_book.id


async def test_get_book_by_id_repo(uowm, migrations):
    book = CreateBookFactory.create()
    async with uowm as uow:
        new_book = await uow.books.create_book(book)
        get_book = await uow.books.get_by_id(new_book.id)
        assert new_book == get_book


async def test_delete_book_by_id_repo(uowm, migrations):
    book = CreateBookFactory.create()
    async with uowm as uow:
        new_book = await uow.books.create_book(book)
        await uow.books.delete_by_id(new_book.id)
        with pytest.raises(NoResultFound):
            await uow.books.get_by_id(new_book.id)


async def test_books_list_without_tag_repo(uowm, migrations):
    book = CreateBookFactory.create()
    async with uowm as uow:
        await uow.books.create_book(book)
        assert await uow.books.books_list_without_tag()


@pytest.mark.skip('TODO:')
async def test_books_list_tag_filter_repo(uowm, migrations):
    async with uowm as uow:
        await uow.books.books_list()
        await uow.books.books_list(tag=1)
