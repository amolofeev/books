from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Optional


class ITagsDAO(ABC, metaclass=ABCMeta):
    @abstractmethod
    async def tags_list(self) -> list[Any]:
        ...

    @abstractmethod
    async def tags_for_book_by_book_id(self, pk: int) -> list[Any]:
        ...

    @abstractmethod
    async def delete_tags_for_book(self, pk: int):
        ...

    @abstractmethod
    async def set_tags_for_book(self, pk: int, tags: list[int]):
        ...
