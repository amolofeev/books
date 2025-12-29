from pathlib import Path

from src.di.container import UnitOfWork
from src.domain.factory.book import BookDTOFactory
from src.domain.services.book import create_book, delete_book


FILE = Path("/www/media/test.txt")
COVER = Path("/www/media/test.png")


async def test_delete_exists_book(uow: UnitOfWork) -> None:
    book = await create_book(file=FILE, cover=COVER)

    await delete_book(book.id)

    assert not await uow.storage.exists(book.file)
    assert not await uow.storage.exists(book.cover)


async def test_delete_not_exists_book(uow: UnitOfWork) -> None:
    book = BookDTOFactory.create()
    # without error
    await delete_book(book.id)
