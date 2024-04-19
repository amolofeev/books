import logging
import os
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, UploadFile
from pydantic import BaseModel
from starlette.responses import HTMLResponse, RedirectResponse, Response

from src.dao.books import BooksDAO
from src.dao.m2m_tag_book import M2MTagBookDAO
from src.dao.tags import TagsDAO
from src.dependencies import pg_pool_dep, template
from src.interface.books import IBookDAO
from src.interface.tags import ITagsDAO
from src.repository.books import BookRepository
from src.repository.m2m_tag_book import M2MTagBookRepository
from src.repository.tags import TagsRepository
from src.vars import PGConnection


logger = logging.getLogger(__file__)
router = APIRouter(prefix='/books')


class GodObject:
    books: IBookDAO = BookRepository(BooksDAO())
    tags: ITagsDAO = TagsRepository(TagsDAO())
    m2m: M2MTagBookDAO = M2MTagBookRepository(M2MTagBookDAO())


uow = GodObject()


@router.get('/', response_class=HTMLResponse)
async def books_list(
        tag: Optional[int] = None,
        pool=Depends(pg_pool_dep),
        tpl=Depends(template('list.html')),
) -> str:
    async with pool.connect() as conn:
        PGConnection.set(conn)
        if tag is None or tag:
            book_list = await uow.books.books_list(tag)
        else:
            book_list = await uow.books.books_list_without_tag()
        tag_list = await uow.tags.tags_list()
    return tpl.render(books=book_list, tags=tag_list)


@router.post('/')
async def books_create(
        file: UploadFile,
        cover: UploadFile,
        pool=Depends(pg_pool_dep),
) -> dict:
    fid = uuid.uuid4().hex
    _, ext = os.path.splitext(file.filename)
    with open(f'media/files/{fid}{ext}', 'wb') as fp:
        while chunk := await file.read(4096):
            fp.write(chunk)

    _, cover_ext = os.path.splitext(cover.filename)
    with open(f'media/files/{fid}{cover_ext}', 'wb') as fp:
        while chunk := await cover.read(4096):
            fp.write(chunk)
    data = {
        'file': f'/media/files/{fid}{ext}',
        'cover': f'/media/files/{fid}{cover_ext}',
        'filename': file.filename
    }
    async with pool.begin() as conn:
        PGConnection.set(conn)
        data['id'] = await uow.books.create_book(**data)
    return data


@router.get('/{book_id}', response_class=HTMLResponse)
async def books_detail(
        book_id: int,
        tpl=Depends(template('detail.html')),
        pool=Depends(pg_pool_dep),
):
    async with pool.connect() as conn:
        PGConnection.set(conn)
        book = await uow.books.get_by_id(book_id)
        all_tags = await uow.tags.tags_list()
        book_tags = await uow.m2m.get_tags_for_book(book_id)
    return tpl.render(book=book, tags=all_tags, book_tags=book_tags)


@router.post('/{book_id}/delete/', response_class=RedirectResponse)
async def books_delete(
        book_id: int,
        pool=Depends(pg_pool_dep),
):
    async with pool.begin() as conn:
        PGConnection.set(conn)
        await uow.m2m.delete_by_book(book_id)
        print(await uow.books.delete_by_id(book_id))
    return RedirectResponse('/books/', status_code=302)


# TODO: FIXME in next iteration
class UpdateBookDTO(BaseModel):
    book_id: int
    title: str
    tags: Optional[list[int]]


@router.post('/tags/', response_class=RedirectResponse)
async def set_tags(
        dto: UpdateBookDTO,
        pool=Depends(pg_pool_dep),
):
    async with pool.begin() as conn:
        PGConnection.set(conn)
        await uow.books.set_title(dto.book_id, dto.title)
        await uow.m2m.delete_by_book(dto.book_id)
        if dto.tags:
            await uow.m2m.set_tags_for_book(dto.book_id, dto.tags)
    return Response('', status_code=204)
