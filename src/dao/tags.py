from typing import Any

import msgspec
import sqlalchemy as sa

from src.db.public import m2m_tag_book, tags
from src.dto.tags import TagDTO, TagWithActiveDTO
from src.interface.tags import ITagsDAO
from src.vars import PGConnection


class TagsDAO(ITagsDAO):
    async def tags_list(self) -> list[TagDTO]:
        conn = PGConnection.get()

        topq = (
            sa.select(tags)
            .cte('cte', recursive=True)
        )

        bottomq = (
            sa.select(tags)
            .join(topq, tags.c.parent_id == topq.c.id)
        )
        recursive_q = topq.union(bottomq)
        query = (
            sa.select(
                recursive_q
            )
            .order_by(sa.nullsfirst(recursive_q.c.parent_id), recursive_q.c.name.asc())
        )
        rows = (await conn.execute(query)).fetchall()
        return msgspec.convert(rows, list[TagDTO])

    async def tags_for_book_by_book_id(self, pk: int) -> list[Any]:
        conn = PGConnection.get()
        rows = (await conn.execute(
            sa.select(
                tags, (m2m_tag_book.c.book_id.is_not(None)).label('is_active'))
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
        return msgspec.convert(rows, list[TagWithActiveDTO])
