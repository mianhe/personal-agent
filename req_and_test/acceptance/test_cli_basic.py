import pytest
import sys
import os
from io import StringIO
from unittest.mock import patch

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from cli.cli import CommandLineInterface

@pytest.fixture
def cli():
    """提供CLI实例"""
    return CommandLineInterface()

class TestCLIStartup:
    """CLI启动测试"""
    
    def test_should_display_welcome_message_on_startup(self, cli):
        """测试启动时显示欢迎信息"""
        with patch('builtins.input', return_value="/exit"):
            with StringIO() as stdout:
                sys.stdout = stdout
                cli.start()
                output = stdout.getvalue()
                assert "Welcome to Personal Agent CLI!" in output
                assert "Type /help for available commands" in output

class TestCLICommandParsing:
    """CLI命令解析测试"""

    @pytest.mark.parametrize("command,expected_outputs", [
        ("/help", ["Available CLI commands:", "/help", "/exit", "/clear"]),
        ("/exit", ["Goodbye!"]),
        ("/clear", ["Welcome to Personal Agent CLI!"]),
        ("/unknown", ["Unknown command: unknown", "Available commands:"]),
        ("/HELP", ["Available CLI commands:"]),  # 测试大小写不敏感
        ("", [])  # 空输入应该被忽略
    ])
    def test_command_handling(self, cli, command, expected_outputs):
        """测试命令处理"""
        # 直接测试命令处理
        with StringIO() as stdout:
            sys.stdout = stdout
            
            if command.startswith("/"):
                cli._handle_cli_command(command[1:])
            else:
                cli.process_input(command)
                
            output = stdout.getvalue()
            for expected in expected_outputs:
                assert expected in output
            
            # 检查只有 exit 命令会改变运行状态
            if command == "/exit":
                assert not cli.running
            else:
                assert cli.running


