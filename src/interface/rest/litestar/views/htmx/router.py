import aioprometheus
from litestar import Router, get
from litestar.response import Template, Response

from src.domain.services.book import get_list_by_category_id
from src.domain.services.category import get_default_category
from .authors import AuthorsHandler
from .books import BooksHandler
from .categories import CategoriesHandler


@get(path='/')
async def index() -> Template:
    default_category = await get_default_category()
    books_in_default_category = await get_list_by_category_id(default_category)
    return Template(
        'index.html',
        context={
            'books': books_in_default_category,
        }
    )


@get('/healthcheck')
async def healthcheck() -> dict:
    return {}


@get('/metrics')
async def metrics() -> Response[bytes]:
    body, headers = aioprometheus.render(aioprometheus.REGISTRY, [])
    return Response(
        body,
        headers=headers
    )


router = Router(
    path='/',
    route_handlers=[
        healthcheck,
        metrics,
        index,
        AuthorsHandler,
        BooksHandler,
        CategoriesHandler,
    ]
)
