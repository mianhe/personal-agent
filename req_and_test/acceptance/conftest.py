"""共享的测试夹具。"""

import pytest

from core.chat_svc_init import create_chat_service
from cli.cli import CommandLineInterface


@pytest.fixture
def cli():
    """提供CLI实例"""
    chat_service = create_chat_service()  # 使用新的初始化函数
    return CommandLineInterface(chat_service)
