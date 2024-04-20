from typing import Optional

import msgspec
import sqlalchemy as sa

from src.db.public import books, m2m_tag_book, tags
from src.dto.books import BookDTO, CreateBookDTO
from src.interface.books import IBookDAO
from src.vars import PGConnection


class BooksDAO(IBookDAO):
    async def books_list(self, tag: Optional[int] = None) -> list[BookDTO]:
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
        result = (await conn.execute(query.order_by(books.c.filename, books.c.id))).fetchall()
        return msgspec.convert(result, list[BookDTO])

    async def books_list_without_tag(self) -> list[BookDTO]:
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
            .where(m2m_tag_book.c.book_id == None)  # pylint: disable=singleton-comparison
        )
        result = (await conn.execute(query.order_by(books.c.filename, books.c.id))).fetchall()
        return msgspec.convert(result, list[BookDTO])

    async def get_by_id(self, pk: int) -> BookDTO:
        conn = PGConnection.get()
        result = (await conn.execute(sa.select(books).where(books.c.id == pk))).one()
        return msgspec.convert(result, BookDTO)

    async def set_title(self, pk: int, title: str):
        conn = PGConnection.get()
        await conn.execute(
            books.update()
            .where(books.c.id == pk)
            .values(title=title)
        )

    async def create_book(self, book: CreateBookDTO) -> BookDTO:
        conn = PGConnection.get()
        row = (
            await conn.execute(
                sa.insert(books)
                .values(
                    file=book.file,
                    cover=book.cover,
                    filename=book.filename,
                    title=(book.title or book.filename),
                )
                .returning(books)
            )
        ).one()
        return msgspec.convert(row, BookDTO)

    async def delete_by_id(self, pk: int) -> None:
        conn = PGConnection.get()
        await conn.execute(
            sa.delete(books)
            .where(
                books.c.id == pk
            )
        )
