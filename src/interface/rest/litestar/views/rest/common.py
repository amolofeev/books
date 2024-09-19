import asyncio
import random

from litestar import Controller, Response, delete, get, patch, post, put

from src.domain.services.test import blahblah


class TestHandler(Controller):
    path = "/test"

    @get(path='/test')
    async def a_test(self) -> None:
        await blahblah()

    @get(path="/get/{status_code:int}/{latency:float}")
    async def get(self, status_code: int, latency: float) -> Response:
        if random.random() <= latency:
            await asyncio.sleep(random.random())
        return Response(None, status_code=status_code)

    @post(path="/post/{status_code:int}/{latency:float}")
    async def post(self, status_code: int, latency: float) -> Response:
        if random.random() <= latency:
            await asyncio.sleep(random.random())
        return Response(None, status_code=status_code)

    @put(path="/put/{status_code:int}/{latency:float}")
    async def put(self, status_code: int, latency: float) -> Response:
        if random.random() <= latency:
            await asyncio.sleep(random.random())
        return Response(None, status_code=status_code)

    @patch(path="/patch/{status_code:int}/{latency:float}")
    async def patch(self, status_code: int, latency: float) -> Response:
        if random.random() <= latency:
            await asyncio.sleep(random.random())
        return Response(None, status_code=status_code)

    @delete(path="/delete/{status_code:int}/{latency:float}", status_code=204)
    async def delete(self, status_code: int, latency: float) -> None:
        if random.random() <= latency:
            await asyncio.sleep(random.random())
        return Response(None, status_code=status_code)
