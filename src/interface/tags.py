from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Optional

from src.dto.tags import TagDTO


class ITagsDAO(ABC, metaclass=ABCMeta):
    @abstractmethod
    async def tags_list(self) -> list[TagDTO]:
        ...

    @abstractmethod
    async def tags_for_book_by_book_id(self, pk: int) -> list[Any]:
        ...
