import logging
import os
import uuid
from typing import Optional

import msgspec.json
from dependency_injector.wiring import Provide, inject
from pydantic import BaseModel
from starlette.responses import HTMLResponse, RedirectResponse, Response

from fastapi import APIRouter, Depends, UploadFile
from src.domain.dto.books import BookDTO, CreateBookDTO


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
    _, book_fname = os.path.split(file.filename)
    with open(f'media/files/{book_fname}', 'wb') as fp:
        while chunk := await file.read(4096):
            fp.write(chunk)

    _, cover_fname = os.path.split(cover.filename)
    with open(f'media/files/{cover_fname}', 'wb') as fp:
        while chunk := await cover.read(4096):
            fp.write(chunk)

    async with uowm as uow:
        book = await uow.books.create_book(
            CreateBookDTO(
                file=f'/media/files/{book_fname}',
                cover=f'/media/files/{cover_fname}',
                filename=book_fname,
                title=book_fname
            )
        )
    return msgspec.to_builtins(book)


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
    import pathlib
    async with uowm as uow:
        book: BookDTO = await uow.books.get_by_id(book_id)
        filepath = pathlib.Path(f'/www{book.file}')
        coverpath = pathlib.Path(f'/www{book.cover}')
        if filepath.exists():
            os.remove(filepath)
        if coverpath.exists():
            os.remove(coverpath)
        await uow.m2m.delete_by_book(book_id)
        await uow.books.delete_by_id(book_id)
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
