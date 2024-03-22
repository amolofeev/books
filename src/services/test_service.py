# TODO: for test purposes only. remove in next iteration
from dependency_injector.wiring import Provide


async def test_di_value(value: str = Provide['test']) -> str:
    return value
