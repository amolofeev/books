from typing import Awaitable, Callable

from fastapi import FastAPI

from src.di.container import init_container


def create_engine(app: FastAPI) -> Callable[[], Awaitable]:
    """decorator"""

    async def __wrap__():
        """store engine in app.state"""
        app.state.container = await init_container()
    return __wrap__


def close_engine(app: FastAPI) -> Callable[[], Awaitable]:
    """decorator"""

    async def __wrap__() -> None:
        """close db engine"""
        await app.state.container.shutdown_resources()

    return __wrap__
