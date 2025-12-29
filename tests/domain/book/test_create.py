from pathlib import Path

from src.di.container import UnitOfWork
from src.domain.services.book import create_book


FILE = Path("/www/media/test.txt")
COVER = Path("/www/media/test.png")


async def test_create_book(uow: UnitOfWork) -> None:
    new_book = await create_book(file=FILE, cover=COVER)
    assert new_book


async def test_recreate_book(uow: UnitOfWork) -> None:
    """Если hash(id) не уникальный, возвращаем ту что лежит в БД."""
    new_book = await create_book(file=FILE, cover=COVER)
    same_book = await create_book(file=FILE, cover=COVER)
    assert new_book == same_book
