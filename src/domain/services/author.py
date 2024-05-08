from typing import AsyncGenerator

from dependency_injector.wiring import Provide, inject

from src.di.container import UnitOfWork
from src.domain.dto.author import AuthorDTO


@inject
async def create_author(
        name: str,
        uow: UnitOfWork = Provide['uow'],
) -> AuthorDTO:
    async with uow:
        return await uow.author.create(name)