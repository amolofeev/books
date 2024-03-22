from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.views",
            "src.services",
        ]
    )
    test = providers.Object("PRODUCTION")


def init_container(**kwargs):
    defaults = {
        **kwargs,
    }
    return Container(**defaults)
