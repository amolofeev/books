# pylint: disable=c-extension-no-member
from dependency_injector import containers


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.views",
            "src.services",
        ]
    )


def init_container(**kwargs):
    defaults = {
        **kwargs,
    }
    return Container(**defaults)
