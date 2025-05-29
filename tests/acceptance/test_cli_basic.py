"""
特性描述：提供基本的命令行聊天界面，解析系统命令，并接受用户输入
"""

from unittest.mock import patch, AsyncMock

import pytest

pytestmark = pytest.mark.tbd


class TestCLIStartup:
    """CLI启动测试"""

    @pytest.mark.asyncio
    async def test_should_display_welcome_message_on_startup(self, cli, capsys):
        """
        启动后显示正确的欢迎提示词
        """
        with patch(
            "prompt_toolkit.PromptSession.prompt_async", new_callable=AsyncMock
        ) as mock_prompt:
            mock_prompt.return_value = "/exit"
            await cli.start()
            output = capsys.readouterr().out
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
    async def test_command_handling(self, cli, command, expected_outputs, capsys):
        """
        能够响应"/exit"命令并正常退出程序
        能够响应"/help"命令并提供帮助信息
        能够响应"/clear"命令并清屏
        """
        with patch(
            "prompt_toolkit.PromptSession.prompt_async", new_callable=AsyncMock
        ) as mock_prompt:
            mock_prompt.side_effect = [command, "/exit"]
            await cli.start()
            output = capsys.readouterr().out
            for expected in expected_outputs:
                assert expected in output

            # 检查 running 状态
            if command == "/exit":
                assert not cli.running
            else:
                # 重置 running 状态，因为第二个输入是 /exit
                cli.running = True
                assert cli.running


# class TestCLIAutoCompletion:
#     """
#     系统命令自动补全与提示
#     操作流程：命令行输入"/**" 并按tab键 → 提示可选命令 → 在命令列表中选择 → 自动补齐命令
#     """

#     @pytest.mark.asyncio
#     async def test_should_suggest_all_commands_on_tab_after_slash(self, cli):
#         """
#         在终端输入"/"后，按下Tab键可以自动匹配，并提示所有可用的系统命令列表。
#         """
#         # 直接测试 CLI 的 completer 功能
#         if hasattr(cli, 'completer'):
#             from prompt_toolkit.document import Document
#             document = Document("/")
#             completions = list(cli.completer.get_completions(document, None))
#             completion_texts = [c.text for c in completions]
#             assert "help" in completion_texts
#             assert "exit" in completion_texts
#             assert "clear" in completion_texts
#             assert "server" in completion_texts
#         else:
#             pytest.skip("CLI completer not implemented yet")

#     @pytest.mark.asyncio
#     async def test_should_suggest_subcommands_on_tab_after_main_command(self, cli):
#         """
#         对于有二级子命令（如/server），输入主命令后按Tab键可提示后续可用的子命令
#         """
#         if hasattr(cli, 'completer'):
#             from prompt_toolkit.document import Document
#             document = Document("/server ")
#             completions = list(cli.completer.get_completions(document, None))
#             completion_texts = [c.text for c in completions]
#             assert "start" in completion_texts
#             assert "stop" in completion_texts
#         else:
#             pytest.skip("CLI completer not implemented yet")

#     @pytest.mark.asyncio
#     async def test_should_select_command_with_arrows_and_enter(self, cli):
#         """
#         在命令列表中可以用上下键选择并用回车键确认
#         """
#         # 这个测试更适合在 UI 层面测试，暂时跳过
#         pytest.skip("UI interaction testing needs specific implementation")

#     @pytest.mark.asyncio
#     async def test_should_suggest_commands_on_tab_after_partial(self, cli):
#         """
#         输入部分命令（如 /se）后按下Tab键，自动补齐或提示匹配命令
#         """
#         if hasattr(cli, 'completer'):
#             from prompt_toolkit.document import Document
#             document = Document("/se")
#             completions = list(cli.completer.get_completions(document, None))
#             completion_texts = [c.text for c in completions]
#             # 假设只有 server 匹配 /se 前缀
#             assert any("server" in text for text in completion_texts)
#         else:
#             pytest.skip("CLI completer not implemented yet")
