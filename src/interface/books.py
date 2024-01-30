from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Optional


class IBookDAO(ABC, metaclass=ABCMeta):
    @abstractmethod
    async def books_list(self, tag: Optional[str] = None) -> list[Any]:
        ...

    @abstractmethod
    async def get_by_id(self, pk: int) -> Any:
        ...

    @abstractmethod
    async def set_title(self, pk: int, title: str):
        ...

    @abstractmethod
    async def create_book(self, file: str, cover: str, filename: str) -> int:
        ...
