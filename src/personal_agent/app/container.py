# pylint: disable=no-member
"""
顶层 container，负责生成和组装其他容器，并创建实例供使用

"""

from dependency_injector import containers, providers
from personal_agent.config import ConfigContainer
from personal_agent.chat import Container as ChatContainer
from personal_agent.cli import Container as CliContainer


class AppContainer(containers.DeclarativeContainer):

    # 生成 config 的容器
    config_container = providers.Container(ConfigContainer)
    configer = config_container.provided.configer

    # 注入 configer 的 provider到 chat 容器中，生成 chat 的容器，并获取它的 chat_service 的 provider
    chat_container = providers.Container(ChatContainer, configer=configer)
    chat_service = chat_container.provided.chat_service

    # 注入 chat_service 的 provider到 cli 容器中，生成 cli 的容器，并创建 cli 的实例
    cli_container = providers.Container(CliContainer, chat_service=chat_service)
    cli_bot = cli_container.provided.cli()
