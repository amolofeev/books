from abc import ABC, ABCMeta, abstractmethod
from typing import Optional

from src.domain.dto.books import BookDTO, CreateBookDTO


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
    async def create_book(self, book: CreateBookDTO) -> BookDTO:
        ...

    @abstractmethod
    async def delete_by_id(self, pk: int) -> None:
        ...
