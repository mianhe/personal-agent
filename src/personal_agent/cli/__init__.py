"""
cli 子系统职责：用户操作界面，作为用户交互的入口，负责接受并回复用户消息，以及接受并回复用户输入的系统命令。
"""

from .container import Container
from .api.cli_service import CommandLineInterface

__all__ = ["Container", "CommandLineInterface"]
