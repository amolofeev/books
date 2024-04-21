from src.domain.interface.m2m_tag_book import I_m2m_tag_book_DAO


class M2MTagBookRepository(I_m2m_tag_book_DAO):
    def __init__(self, dao: I_m2m_tag_book_DAO):
        self._dao = dao

    async def insert(self, book_id: int, tag_id: int) -> None:
        return await self._dao.insert(book_id, tag_id)

    async def delete(self, book_id: int, tag_id: int) -> None:
        return await self._dao.delete(book_id, tag_id)

    async def delete_by_book(self, book_id: int) -> None:
        return await self._dao.delete_by_book(book_id)

    async def delete_by_tag(self, tag_id: int) -> None:
        return await self._dao.delete_by_tag(tag_id)

    async def get_tags_for_book(self, book_id: int) -> list[int]:
        return await self._dao.get_tags_for_book(book_id)

    async def get_books_for_tag(self, tag_id: int) -> list[int]:
        return await self._dao.get_books_for_tag(tag_id)

    async def set_tags_for_book(self, book_id: int, tags: list[int]):
        return await self._dao.set_tags_for_book(book_id, tags)
