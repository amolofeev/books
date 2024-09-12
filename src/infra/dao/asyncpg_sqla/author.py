import uuid

import msgspec
import sqlalchemy as sa

from src.domain.dto.author import AuthorDTO
from src.domain.interface.author import IAuthorDAO
from src.infra.db.postgresql.public import author, m2m_author_book
from src.vars import PGConnection


class AuthorAsyncpgSQLADAO(IAuthorDAO):
    async def create(self, name: str) -> AuthorDTO:
        conn = PGConnection.get()
        stmt = (
            sa.insert(author)
            .values(name=name)
            .returning(author)
        )
        new_row = (await conn.execute(stmt)).one()
        return msgspec.convert(new_row, AuthorDTO)

    async def get_list_by_book_id(self, book_id: uuid.UUID | str) -> list[AuthorDTO]:
        conn = PGConnection.get()
        stmt = (
            sa.select(author)
            .join(m2m_author_book, m2m_author_book.c.book_id == book_id)
        )
        rows = (await conn.execute(stmt)).fetchall()
        return msgspec.convert(rows, list[AuthorDTO])
