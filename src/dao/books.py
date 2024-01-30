from typing import Any, Optional

import sqlalchemy as sa

from src.db.public import books, m2m_tag_book, tags
from src.interface.books import IBookDAO
from src.vars import PGConnection


class BooksDAO(IBookDAO):
    async def books_list(self, tag: Optional[str] = None) -> list[Any]:
        conn = PGConnection.get()
        if tag:
            query = (
                sa.select(books)
                .select_from(
                    books
                    .join(
                        m2m_tag_book,
                        books.c.id == m2m_tag_book.c.book_id,
                        isouter=True,
                    ).join(
                        tags,
                        tags.c.id == m2m_tag_book.c.tag_id,
                        isouter=True,
                    )
                )
                .where(tags.c.id == tag)
            )
        else:
            query = sa.select(books)
        return (await conn.execute(query.order_by(books.c.filename))).fetchall()

    async def get_by_id(self, pk: int) -> Any:
        conn = PGConnection.get()
        return (await conn.execute(sa.select(books).where(books.c.id == pk))).one()

    async def set_title(self, pk: int, title: str):
        conn = PGConnection.get()
        await conn.execute(
            books.update()
            .where(books.c.id == pk)
            .values(title=title)
        )

    async def create_book(self, file: str, cover: str, filename: str) -> int:
        conn = PGConnection.get()
        return (
            await conn.execute(
                sa.insert(books)
                .values(file=file, cover=cover, filename=filename)
                .returning(books.c.id)
            )
        ).scalars().one()
