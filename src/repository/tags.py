from typing import Any

from src.dto.tags import TagDTO
from src.interface.tags import ITagsDAO


class TagsRepository(ITagsDAO):

    def __init__(self, dao: ITagsDAO):
        self.dao = dao

    async def tags_for_book_by_book_id(self, pk: int) -> list[Any]:
        return await self.dao.tags_for_book_by_book_id(pk)

    async def tags_list(self) -> list[TagDTO]:
        return await self.dao.tags_list()
