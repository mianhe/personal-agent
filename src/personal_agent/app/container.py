# pylint: disable=no-member
"""
顶层 container，负责生成和组装其他容器，并创建实例供使用

"""

from dependency_injector import containers, providers
from personal_agent.config import ConfigContainer
from personal_agent.chat import Container as ChatContainer
from personal_agent.cli import Container as CliContainer
from personal_agent.mcp import Container as MCPContainer


class AppContainer(containers.DeclarativeContainer):

    # 生成 config 的容器
    config_container = providers.Container(ConfigContainer)
    configer = config_container.provided.configer

    # 注入 configer 的 provider到 chat 容器中，生成 chat 的容器，并获取它的 chat_service 的 provider
    chat_container = providers.Container(ChatContainer, configer=configer)
    chat_service = chat_container.provided.chat_service

    mcp_container = providers.Container(MCPContainer)
    server_registry = mcp_container.provided.server_registry

    cli_container = providers.Container(
        CliContainer, server_registry=server_registry, chat_service=chat_service
    )
    cli = cli_container.provided.cli()
