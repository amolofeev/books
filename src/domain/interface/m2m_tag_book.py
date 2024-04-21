from abc import ABC, ABCMeta, abstractmethod


class I_m2m_tag_book_DAO(ABC, metaclass=ABCMeta):
    @abstractmethod
    async def insert(self, book_id: int, tag_id: int) -> None:
        ...

    @abstractmethod
    async def delete(self, book_id: int, tag_id: int) -> None:
        ...

    @abstractmethod
    async def delete_by_book(self, book_id: int) -> None:
        ...

    @abstractmethod
    async def delete_by_tag(self, tag_id: int) -> None:
        ...

    @abstractmethod
    async def get_tags_for_book(self, book_id: int) -> list[int]:
        ...

    @abstractmethod
    async def get_books_for_tag(self, tag_id: int) -> list[int]:
        ...

    @abstractmethod
    async def set_tags_for_book(self, book_id: int, tags: list[int]):
        ...
