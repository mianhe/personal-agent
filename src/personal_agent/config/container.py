from dependency_injector import containers, providers
from .config import FileConfigSupplier


class ConfigContainer(containers.DeclarativeContainer):
    configer = providers.Singleton(FileConfigSupplier)
