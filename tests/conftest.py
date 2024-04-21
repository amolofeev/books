# pylint: disable=redefined-outer-name,C0413
from typing import AsyncGenerator

import pytest

from src.di.container import UnitOfWork, init_container


@pytest.fixture
async def container():
    container = await init_container()
    yield container
    await container.shutdown_resources()


@pytest.fixture
async def transaction(container) -> AsyncGenerator[UnitOfWork, None]:
    transaction = await container.transaction()
    yield transaction
