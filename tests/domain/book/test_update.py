from src.domain.factory.book import BookDTOFactory
from src.domain.services.book import update_book


async def test_partial_update(pg_container, uow):
    book = BookDTOFactory.create(title='old title')
    async with uow:
        await uow.book.create(book)

    new_title = 'new title'
    updated_book = await update_book(book.id, title=new_title)
    assert updated_book.book.title == new_title
