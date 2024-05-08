import uuid
from abc import ABC, ABCMeta, abstractmethod

from src.domain.dto.category import CategoryDTO


class ICategoryDAO(ABC, metaclass=ABCMeta):
    @abstractmethod
    async def create(self, name: str, parent_id: int = None) -> CategoryDTO:
        ...

    @abstractmethod
    async def get_list_by_book_id(self, book_id: uuid.UUID|str) -> list[CategoryDTO]:
        ...

    @abstractmethod
    async def get_list(self) -> list[CategoryDTO]:
        ...

    @abstractmethod
    async def get_default_category_id(self) -> int:
        ...