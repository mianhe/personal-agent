from dependency_injector import containers, providers
from .cli import CommandLineInterface


class Container(containers.DeclarativeContainer):
    chat_service = providers.Dependency()
    server_registry = providers.Dependency()
    cli = providers.Singleton(
        CommandLineInterface, server_registry=server_registry, chat_service=chat_service
    )
