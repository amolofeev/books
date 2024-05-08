from litestar import Controller, Request, get
from litestar.response import Template


class AuthorsHandler(Controller):
    path = '/authors'

    @get(path='/')
    async def index(self, request: Request) -> Template:
        return Template('books/index.html')