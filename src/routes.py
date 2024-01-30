from fastapi import FastAPI

from .views import books, common


def init_routes(application: FastAPI):
    application.include_router(common.router)
    application.include_router(books.router)
