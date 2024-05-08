import uuid

import sqlalchemy.dialects.postgresql as pg_sa
import sqlalchemy as sa
from src.domain.interface.m2m_category_book import IM2MCategoryBookDAO
from src.infra.db.postgresql.public import m2m_category_book
from src.vars import PGConnection


class M2MCategoryBookAsyncpgSQLADAO(IM2MCategoryBookDAO):
    async def set_categories_for_book(
            self,
            book_id: uuid.UUID | str,
            categories: list[int],
    ) -> None:
        conn = PGConnection.get()
        rm_stmt = (
            sa.delete(m2m_category_book)
            .where(
                sa.and_(
                    m2m_category_book.c.book_id == book_id,
                    m2m_category_book.c.category_id.notin_(categories)
                )
            )
        )
        await conn.execute(rm_stmt)

        if categories:
            add_stmt = (
                pg_sa.insert(m2m_category_book)
                .on_conflict_do_nothing(index_elements=['book_id', 'category_id'])
            )
            await conn.execute(
                add_stmt,
                [
                    {'book_id': book_id, 'category_id': category_id}
                    for category_id in categories
                ]
            )

    async def create(self, category_id: int, book_id: uuid.UUID | str) -> None:
        conn = PGConnection.get()
        stmt = (
            pg_sa.insert(m2m_category_book)
            .values(category_id=category_id, book_id=book_id)
            .on_conflict_do_nothing(index_elements=['category_id', 'book_id'])
        )
        await conn.execute(stmt)

    async def delete(self, category_id: int, book_id: uuid.UUID | str) -> None:
        raise NotImplementedError(self.delete)
