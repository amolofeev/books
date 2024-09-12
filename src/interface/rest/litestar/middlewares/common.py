from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from asgiref.typing import ASGIApplication


def path_to_route_name(app: ASGIApplication, path: str) -> str:
    app, handler, path, params = app.asgi_router.handle_routing(path, "OPTIONS")
    return next(iter(handler.paths))
