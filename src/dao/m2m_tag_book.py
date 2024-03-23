import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg_sa

from src.db.public import m2m_tag_book
from src.interface.m2m_tag_book import I_m2m_tag_book_DAO
from src.vars import PGConnection


class M2MTagBookDAO(I_m2m_tag_book_DAO):
    async def set_tags_for_book(self, book_id: int, tags: list[int]):
        await self.delete_by_book(book_id)

        if not tags:
            return

        conn = PGConnection.get()
        await conn.execute(
            m2m_tag_book.insert()
            .values(
                [
                    dict(tag_id=tag_id, book_id=book_id)
                    for tag_id in tags
                ]
            )
        )

    async def get_books_for_tag(self, tag_id: int) -> list[int]:
        conn = PGConnection.get()
        stmt = (
            sa.select(m2m_tag_book.c.book_id)
            .where(m2m_tag_book.c.tag_id == tag_id)
        )

        return (await conn.execute(stmt)).scalars().fetchall()

    async def get_tags_for_book(self, book_id: int) -> list[int]:
        conn = PGConnection.get()
        stmt = (
            sa.select(m2m_tag_book.c.tag_id)
            .where(m2m_tag_book.c.book_id == book_id)
        )

        return (await conn.execute(stmt)).scalars().fetchall()

    async def delete_by_tag(self, tag_id: int) -> None:
        conn = PGConnection.get()
        stmt = (
            sa.delete(m2m_tag_book)
            .where(m2m_tag_book.c.tag_id == tag_id)
        )

        await conn.execute(stmt)

    async def delete_by_book(self, book_id: int) -> None:
        conn = PGConnection.get()
        stmt = (
            sa.delete(m2m_tag_book)
            .where(m2m_tag_book.c.book_id == book_id)
        )

        await conn.execute(stmt)

    async def delete(self, book_id: int, tag_id: int) -> None:
        conn = PGConnection.get()
        stmt = (
            sa.delete(m2m_tag_book)
            .where(
                sa.and_(
                    m2m_tag_book.c.book_id == book_id,
                    m2m_tag_book.c.tag_id == tag_id
                )
            )
        )

        await conn.execute(stmt)

    async def insert(self, book_id: int, tag_id: int) -> None:
        conn = PGConnection.get()
        stmt = (
            pg_sa.insert(m2m_tag_book)
            .values(book_id=book_id, tag_id=tag_id)
            .on_conflict_do_nothing(index_elements=['book_id', 'tag_id'])
        )

        await conn.execute(stmt)
