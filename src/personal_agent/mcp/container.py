from dependency_injector import containers, providers
from .server_registry_memory import MemoryServerRegistry


class Container(containers.DeclarativeContainer):
    server_registry = providers.Factory(MemoryServerRegistry)
