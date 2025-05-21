from dependency_injector import containers, providers
from .cli import CommandLineInterface


class Container(containers.DeclarativeContainer):
    chat_service = providers.Dependency()
    cli = providers.Singleton(CommandLineInterface, chat_service=chat_service)
