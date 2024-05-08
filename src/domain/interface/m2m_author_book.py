import uuid
from abc import ABC, ABCMeta, abstractmethod


class IM2MAuthorBookDAO(ABC, metaclass=ABCMeta):
    @abstractmethod
    async def create(self, author_id: int, book_id: uuid.UUID | str) -> None:
        ...

    @abstractmethod
    async def delete(self, author_id: int, book_id: uuid.UUID | str) -> None:
        ...