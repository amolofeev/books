# TODO: for test purposes only. remove in next iteration
from dependency_injector import providers

from src.di.container import Container
from src.services.test_service import test_di_value


async def test_di_wiring():
    container = Container()

    base_value = await test_di_value()
    assert base_value == 'PRODUCTION'
    with container.test.override(providers.Object('MOCKED')):
        base_value = await test_di_value()
        assert base_value == 'MOCKED'
    base_value = await test_di_value()
    assert base_value == 'PRODUCTION'


async def test_di_stub_fixture(container):
    base_value = await test_di_value()
    assert base_value == 'MOCKED'
