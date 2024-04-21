from typing import Optional

from src.domain.dto.books import BookDTO, CreateBookDTO
from src.domain.interface.books import IBookDAO


class BookRepository(IBookDAO):
    def __init__(self, dao: IBookDAO):
        self.dao = dao

    async def set_title(self, pk: int, title: str):
        return await self.dao.set_title(pk, title)

    async def get_by_id(self, pk: int) -> BookDTO:
        return await self.dao.get_by_id(pk)

    async def books_list(self, tag: Optional[int] = None) -> list[BookDTO]:
        return await self.dao.books_list(tag)

    async def books_list_without_tag(self) -> list[BookDTO]:
        return await self.dao.books_list_without_tag()

    async def create_book(self, book: CreateBookDTO) -> BookDTO:
        return await self.dao.create_book(book)

    async def delete_by_id(self, pk: int) -> None:
        return await self.dao.delete_by_id(pk)
