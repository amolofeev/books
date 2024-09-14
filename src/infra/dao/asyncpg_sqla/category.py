import uuid

import msgspec
import sqlalchemy as sa

from src.domain.dto.category import CategoryDTO
from src.domain.interface.category import ICategoryDAO
from src.infra.db.postgresql.public import category, m2m_category_book
from src.vars import PGConnection


DEFAULT_CATEGORY_NAME = "-----"


class CategoryAsyncpgSQLADAO(ICategoryDAO):
    async def get_list(self) -> list[CategoryDTO]:
        conn = PGConnection.get()

        topq = (
            sa.select(category)
            .where(
                sa.and_(
                    category.c.parent_id.is_(None),
                ),
            )
            .cte("cte", recursive=True)
        )

        bottomq = (
            sa.select(
                category.c.id,
                sa.func.concat_ws(" - ", topq.c.name, category.c.name),
                category.c.parent_id,
            )
            .join(topq, category.c.parent_id == topq.c.id)
        )
        recursive_q = topq.union(bottomq)
        query = (
            sa.select(
                recursive_q
            )
            .order_by(recursive_q.c.name)
        )
        rows = (await conn.execute(query)).fetchall()
        return msgspec.convert(rows, list[CategoryDTO])

    async def create(self, name: str, parent_id: int | None = None) -> CategoryDTO:
        conn = PGConnection.get()
        stmt = (
            sa.insert(category)
            .values(name=name, parent_id=parent_id)
            .returning(category)
        )
        row = (await conn.execute(stmt)).one()
        return msgspec.convert(row, CategoryDTO)

    async def get_list_by_book_id(self, book_id: uuid.UUID | str) -> list[CategoryDTO]:
        conn = PGConnection.get()
        stmt = (
            sa.select(category)
            .join(m2m_category_book, m2m_category_book.c.category_id == category.c.id)
            .where(m2m_category_book.c.book_id == book_id)
        )
        rows = (await conn.execute(stmt)).fetchall()
        return msgspec.convert(rows, list[CategoryDTO])

    async def _exists(self, where) -> bool:
        conn = PGConnection.get()
        stmt = (
            sa.select(
                sa.exists(
                    sa.select(category.c.id)
                    .where(where)
                    .limit(1)
                )
            )
        )
        return (await conn.execute(stmt)).scalars().one()

    async def get_default_category_id(self) -> int:
        conn = PGConnection.get()
        selector = sa.and_(
            category.c.name == DEFAULT_CATEGORY_NAME,
            category.c.parent_id.is_(None),
        )

        if not await self._exists(selector):
            await self.create(DEFAULT_CATEGORY_NAME)
        stmt = (
            sa.select(category.c.id)
            .where(selector)
            .limit(1)
        )
        return (await conn.execute(stmt)).scalars().one()
