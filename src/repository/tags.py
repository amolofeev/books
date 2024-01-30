from typing import Any

from src.interface.tags import ITagsDAO


class TagsRepository(ITagsDAO):

    def __init__(self, dao: ITagsDAO):
        self.dao = dao

    async def set_tags_for_book(self, pk: int, tags: list[int]):
        return await self.dao.set_tags_for_book(pk, tags)

    async def delete_tags_for_book(self, pk: int):
        return await self.dao.delete_tags_for_book(pk)

    async def tags_for_book_by_book_id(self, pk: int) -> list[Any]:
        return await self.dao.tags_for_book_by_book_id(pk)

    async def tags_list(self) -> list[Any]:
        return await self.dao.tags_list()
