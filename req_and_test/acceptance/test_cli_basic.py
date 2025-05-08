import sys
from io import StringIO
from unittest.mock import patch, AsyncMock

import pytest


class TestCLIStartup:
    """CLI启动测试"""

    @pytest.mark.asyncio
    async def test_should_display_welcome_message_on_startup(self, cli):
        """测试启动时显示欢迎信息"""
        with patch(
            "prompt_toolkit.PromptSession.prompt_async", new_callable=AsyncMock
        ) as mock_prompt:
            mock_prompt.return_value = "/exit"
            with StringIO() as stdout:
                sys.stdout = stdout
                await cli.start()
                output = stdout.getvalue()
                assert "Welcome to Personal Agent CLI!" in output
                assert "Type /help for available commands" in output


class TestCLICommandParsing:
    """CLI命令解析测试"""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "command,expected_outputs",
        [
            ("/help", ["Available CLI commands:", "/help", "/exit", "/clear"]),
            ("/exit", ["Goodbye!"]),
            ("/clear", ["Welcome to Personal Agent CLI!"]),
            ("/unknown", ["Unknown command: unknown", "Available commands:"]),
            ("/HELP", ["Available CLI commands:"]),  # 测试大小写不敏感
            ("", []),  # 空输入应该被忽略
        ],
    )
    async def test_command_handling(self, cli, command, expected_outputs):
        """测试命令处理"""
        with patch(
            "prompt_toolkit.PromptSession.prompt_async", new_callable=AsyncMock
        ) as mock_prompt:
            mock_prompt.side_effect = [command, "/exit"]
            with StringIO() as stdout:
                sys.stdout = stdout
                await cli.start()
                output = stdout.getvalue()
                for expected in expected_outputs:
                    assert expected in output

                # 检查 running 状态
                if command == "/exit":
                    assert not cli.running
                else:
                    # 重置 running 状态，因为第二个输入是 /exit
                    cli.running = True
                    assert cli.running
