from abc import ABC, ABCMeta, abstractmethod
from typing import Optional

from src.dto.books import BookDTO


class IBookDAO(ABC, metaclass=ABCMeta):
    @abstractmethod
    async def books_list(self, tag: Optional[str] = None) -> list[BookDTO]:
        ...

    @abstractmethod
    async def books_list_without_tag(self) -> list[BookDTO]:
        ...

    @abstractmethod
    async def get_by_id(self, pk: int) -> BookDTO:
        ...

    @abstractmethod
    async def set_title(self, pk: int, title: str):
        ...

    @abstractmethod
    async def create_book(self, file: str, cover: str, filename: str) -> int:
        ...

    @abstractmethod
    async def delete_by_id(self, pk: int) -> None:
        ...
