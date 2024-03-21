from typing import Any, Optional

import sqlalchemy as sa

from src.db.public import books, m2m_tag_book, tags
from src.interface.books import IBookDAO
from src.vars import PGConnection


class BooksDAO(IBookDAO):
    async def books_list(self, tag: Optional[int] = None) -> list[Any]:
        conn = PGConnection.get()
        if tag is not None:
            query = (
                sa.select(books)
                .distinct(books.c.filename, books.c.id)
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
        return (await conn.execute(query.order_by(books.c.filename, books.c.id))).fetchall()

    async def books_list_without_tag(self) -> list[Any]:
        conn = PGConnection.get()
        query = (
            sa.select(books)
            .distinct(books.c.filename, books.c.id)
            .select_from(
                books
                .join(
                    m2m_tag_book,
                    books.c.id == m2m_tag_book.c.book_id,
                    isouter=True,
                )
            )
            .where(m2m_tag_book.c.book_id == None)
        )
        return (await conn.execute(query.order_by(books.c.filename, books.c.id))).fetchall()

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

    async def delete_by_id(self, pk: int) -> None:
        conn = PGConnection.get()
        return (
            await conn.execute(
                sa.delete(books)
                .where(
                    books.c.id == pk
                )
                .returning(books.c.id)
            )
        )
