import logging

import sqlalchemy as sa
from dependency_injector.wiring import Provide, inject
from prometheus_client import generate_latest
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.responses import PlainTextResponse, Response

from fastapi import APIRouter, Depends


logger = logging.getLogger(__file__)
router = APIRouter()


class HealthCheckResponse(BaseModel):
    postgres: bool


@router.get('/liveness',
            response_model=HealthCheckResponse,
            responses={500: {'model': HealthCheckResponse}},
            tags=['common'])
@router.get('/readiness',
            response_model=HealthCheckResponse,
            responses={500: {'model': HealthCheckResponse}},
            tags=['common'])
@inject
async def liveness_handler(
        response: Response,
        ouwm: AsyncEngine = Depends(Provide['uow']),
) -> HealthCheckResponse:

    coroutines = {
        'postgres': check_postgres(ouwm)
    }
    service_status = {}
    for service, coroutine in coroutines.items():
        try:
            await coroutine
        except Exception as e:  # pylint: disable=broad-except
            logger.exception(e)
            service_status[service] = False
        else:
            service_status[service] = True
    status_code = 200
    if not all(service_status.values()):
        status_code = 500
    response.status_code = status_code
    return HealthCheckResponse(**service_status)


async def check_postgres(uowm) -> None:
    async with uowm as uow:
        await uow.connection.execute(sa.text('select True;'))


@router.get('/metrics', response_class=PlainTextResponse)
async def metrics() -> str:
    return generate_latest().decode('utf-8')


@router.get('/')
async def index() -> str:
    return "OK"
