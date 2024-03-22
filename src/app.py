from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .di.container import init_container
from .engine import close_engine, create_engine
from .middlewares.metrics import MetricsMiddleware
from .routes import init_routes


def get_application() -> FastAPI:
    """Initialize app"""
    container = init_container()

    application = FastAPI()
    application.container = container

    application.add_event_handler('startup', create_engine(application))
    application.add_event_handler('shutdown', close_engine(application))
    application.mount("/media", StaticFiles(directory="media"), name="static")
    init_routes(application)
    application.add_middleware(MetricsMiddleware)

    from elasticapm.contrib.starlette import ElasticAPM, make_apm_client
    application.add_middleware(ElasticAPM, client=make_apm_client())

    return application


app = get_application()
