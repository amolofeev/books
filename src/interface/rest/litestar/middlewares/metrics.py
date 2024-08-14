from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asgiref.typing import ASGIApplication, ASGIReceiveCallable, ASGISendCallable, Scope

from src.settings import settings


class PrometheusMiddleware:
    def __init__(self, app: "ASGIApplication", **options) -> None:
        self._app = app

    async def __call__(self, scope: "Scope", receive: "ASGIReceiveCallable", send: "ASGISendCallable") -> None:
        labels = {
            'type': scope['type'],
            **settings.log.EXTRA,
        }
        if scope["type"] == "http":
            labels.update(
                {
                    'path': scope['path'],
                    'method': scope['method']
                }
            )
        try:
            await self._app(scope, receive, send)
        except BaseException:
            ...
        else:
            ...
        finally:
            settings.metrics.requests_count.inc(labels)
