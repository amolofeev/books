from typing import Any, Optional

from src.interface.books import IBookDAO


class BookRepository(IBookDAO):
    def __init__(self, dao: IBookDAO):
        self.dao = dao

    async def set_title(self, pk: int, title: str):
        return await self.dao.set_title(pk, title)

    async def get_by_id(self, pk: int) -> Any:
        return await self.dao.get_by_id(pk)

    async def books_list(self, tag: Optional[int] = None) -> list[Any]:
        return await self.dao.books_list(tag)

    async def books_list_without_tag(self) -> list[Any]:
        return await self.dao.books_list_without_tag()

    async def create_book(self, file: str, cover: str, filename: str) -> int:
        return await self.dao.create_book(file, cover, filename)

    async def delete_by_id(self, pk: int) -> None:
        return await self.dao.delete_by_id(pk)
