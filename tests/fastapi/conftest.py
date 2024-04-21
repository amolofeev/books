import pytest

from fastapi.testclient import TestClient
from src.interface.rest.fastapi.app import app


@pytest.fixture
async def application(migrations, container):  # pylint: disable=W0613
    """override dependencies"""
    yield app


@pytest.fixture
async def client(application):  # pylint: disable=redefined-outer-name
    """Test http client"""
    yield TestClient(application)
