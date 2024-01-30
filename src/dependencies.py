from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.requests import Request


async def pg_pool_dep(request: Request) -> AsyncEngine:
    return request.app.state.pg_pool


def template(template_name: str):
    def __wrap__(request: Request):
        return request.app.state.template.get_template(template_name)
    return __wrap__
