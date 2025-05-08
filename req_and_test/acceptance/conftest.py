"""共享的测试夹具。"""

import pytest

from core.cli_initialization import create_chat_service
from cli.cli import CommandLineInterface


def pytest_configure(config):
    """注册自定义标记"""
    config.addinivalue_line("markers", "implemented: 标记已实现的测试用例")


@pytest.fixture
def cli():
    """提供CLI实例"""
    chat_service = create_chat_service()  # 使用新的初始化函数
    return CommandLineInterface(chat_service)
