from typing import Any

import sqlalchemy as sa

from src.db.public import m2m_tag_book, tags
from src.dto.tags import TagDTO
from src.interface.tags import ITagsDAO
from src.vars import PGConnection


class TagsDAO(ITagsDAO):
    async def tags_list(self) -> list[TagDTO]:
        conn = PGConnection.get()
        result = (await conn.execute(sa.select(tags).order_by(tags.c.name))).fetchall()
        return result

    async def tags_for_book_by_book_id(self, pk: int) -> list[Any]:
        conn = PGConnection.get()
        return (await conn.execute(
            sa.select(
                tags.c.id, tags.c.name, (m2m_tag_book.c.book_id.is_not(None)).label('is_active'))
            .select_from(
                tags.join(
                    m2m_tag_book,
                    sa.and_(
                        tags.c.id == m2m_tag_book.c.tag_id,
                        m2m_tag_book.c.book_id == pk,
                    ),
                    isouter=True,
                ))
            .order_by(tags.c.name))
        ).fetchall()
