from dependency_injector import containers, providers
from .chat_service_impl import ChatServiceImpl
from .mock_chat_service import MockChatService
from .llm_adapter import OpenAICompatibleLLMAdapter


class Container(containers.DeclarativeContainer):
    configer = providers.Dependency()

    llm_config = providers.Callable(
        lambda configer: configer().get_llm_config(), configer
    )
    # llm_config = providers.configer().get_llm_config()

    llm_adapter = providers.Singleton(OpenAICompatibleLLMAdapter, llm_config=llm_config)

    chat_service = providers.Singleton(ChatServiceImpl, llm_adapter=llm_adapter)
    mock_chat_service = providers.Singleton(MockChatService)
