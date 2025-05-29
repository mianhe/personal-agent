from abc import ABC, abstractmethod


class ConfigSupplier(ABC):
    @abstractmethod
    def get_llm_config(self):
        pass

    @abstractmethod
    def get_app_config(self):
        pass
