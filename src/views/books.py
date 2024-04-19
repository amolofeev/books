import logging
import os
import uuid
from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, UploadFile
from pydantic import BaseModel
from starlette.responses import HTMLResponse, RedirectResponse, Response


logger = logging.getLogger(__file__)
router = APIRouter(prefix='/books')


@router.get('/', response_class=HTMLResponse)
@inject
async def books_list(
        tag: Optional[int] = None,
        uowm=Depends(Provide['uow']),
        render=Depends(Provide['render']),
) -> str:
    tpl = render.get_template('list.html')
    async with uowm as uow:
        if tag is None or tag:
            book_list = await uow.books.books_list(tag)
        else:
            book_list = await uow.books.books_list_without_tag()
        tag_list = await uow.tags.tags_list()
    return tpl.render(books=book_list, tags=tag_list)


@router.post('/')
@inject
async def books_create(
        file: UploadFile,
        cover: UploadFile,
        uowm=Depends(Provide['uow']),
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

    async with uowm as uow:
        book_id = await uow.books.create_book(
            file_path := f'/media/files/{fid}{ext}',
            cover := f'/media/files/{fid}{cover_ext}',
            filename := file.filename,
        )
    return {
        'id': book_id,
        'file': file_path,
        'cover': cover,
        'filename': filename,
    }


@router.get('/{book_id}', response_class=HTMLResponse)
@inject
async def books_detail(
        book_id: int,
        uowm=Depends(Provide['uow']),
        render=Depends(Provide['render']),
):
    tpl = render.get_template('detail.html')
    async with uowm as uow:
        book = await uow.books.get_by_id(book_id)
        all_tags = await uow.tags.tags_list()
        book_tags = await uow.m2m.get_tags_for_book(book_id)
    return tpl.render(book=book, tags=all_tags, book_tags=book_tags)


@router.post('/{book_id}/delete/', response_class=RedirectResponse)
@inject
async def books_delete(
        book_id: int,
        uowm=Depends(Provide['uow']),
):
    async with uowm as uow:
        await uow.m2m.delete_by_book(book_id)
        print(await uow.books.delete_by_id(book_id))
    return RedirectResponse('/books/', status_code=302)


# TODO: FIXME in next iteration
class UpdateBookDTO(BaseModel):
    book_id: int
    title: str
    tags: Optional[list[int]]


@router.post('/tags/', response_class=RedirectResponse)
@inject
async def set_tags(
        dto: UpdateBookDTO,
        uowm=Depends(Provide['uow']),
):
    async with uowm as uow:
        await uow.books.set_title(dto.book_id, dto.title)
        await uow.m2m.delete_by_book(dto.book_id)
        if dto.tags:
            await uow.m2m.set_tags_for_book(dto.book_id, dto.tags)
    return Response('', status_code=204)
