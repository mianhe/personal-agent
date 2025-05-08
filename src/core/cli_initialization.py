"""CLI 初始化模块。"""

import asyncio
from core.llm.chat_service_impl import ChatServiceImpl


def create_chat_service():
    """创建聊天服务实例。"""
    return ChatServiceImpl()


def run_cli(chat_service):
    """运行 CLI 界面。"""
    from cli.cli import CommandLineInterface  # 延迟导入以避免循环依赖

    cli = CommandLineInterface(chat_service)
    asyncio.run(cli.start())
