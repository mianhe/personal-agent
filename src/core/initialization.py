"""初始化模块，提供共享的初始化功能。"""

from core.cli_initialization import create_chat_service, run_cli


def initialize_and_run_cli():
    """初始化并运行CLI界面。"""
    chat_service = create_chat_service()
    run_cli(chat_service)
