import uuid
from abc import ABC, ABCMeta, abstractmethod

from src.domain.dto.author import AuthorDTO


class IAuthorDAO(ABC, metaclass=ABCMeta):
    @abstractmethod
    async def create(self, name: str) -> AuthorDTO:
        ...

    @abstractmethod
    async def get_list_by_book_id(self, book_id: uuid.UUID|str) -> list[AuthorDTO]:
        ...
