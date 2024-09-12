from typing import TYPE_CHECKING

from src.interface.rest.litestar.middlewares.common import path_to_route_name


if TYPE_CHECKING:
    from asgiref.typing import ASGIApplication, ASGIReceiveCallable, ASGISendCallable, Scope

from src.settings import settings


class PrometheusMiddleware:
    def __init__(self, app: "ASGIApplication", **options) -> None:
        self._app = app

    async def __call__(self, scope: "Scope", receive: "ASGIReceiveCallable", send: "ASGISendCallable") -> None:
        labels = {
            "type": scope["type"],
            **settings.log.EXTRA,
        }
        if scope["type"] == "http":
            labels.update(
                {
                    "path":  path_to_route_name(scope["app"], scope["path"]),
                    "method": scope["method"],
                },
            )
        try:
            await self._app(scope, receive, send)
        except BaseException:  # noqa: BLE001
            ...
        else:
            ...
        finally:
            settings.metrics.requests_count.inc(labels)
