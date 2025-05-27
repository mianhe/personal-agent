# pylint: disable=duplicate-code

"""
特性描述：支持连接MCP服务器，这样用户就可以使用 mcp的工具来获取信息和解决问题
"""

from unittest.mock import patch, AsyncMock
import pytest


async def run_cli_with_inputs(cli, capsys, inputs):
    """
    辅助函数：mock prompt_toolkit.PromptSession.prompt_async，依次输入 inputs，返回输出内容
    """
    with patch(
        "prompt_toolkit.PromptSession.prompt_async", new_callable=AsyncMock
    ) as mock_prompt:
        mock_prompt.side_effect = inputs
        await cli.start()
        return capsys.readouterr().out


# 功能点1：配置服务器
@pytest.mark.asyncio
@pytest.mark.dev_ongoing
class TestConfigureServer:
    """
    功能点名称：配置服务器
    操作流程：用户配置服务器，用户查询服务器配置
    """

    async def test_no_server_configured_should_reply_no_server_available(
        self, cli, capsys
    ):
        """
        验收标准：如果没有配置服务器，则回答没有服务器可用
        """
        output = await run_cli_with_inputs(cli, capsys, ["/server list", "/exit"])
        # 提取“服务器列表”部分
        if "服务器列表：" in output:
            server_list_section = output.split("服务器列表：", 1)[1]
            # 只检查服务器条目行
            server_lines = [
                line.strip()
                for line in server_list_section.splitlines()
                if line.strip().startswith("- ")
            ]
            assert all("test" not in line for line in server_lines)
        else:
            # 如果没有服务器列表，说明已被正确删除
            assert "没有服务器可用" in output or "No server available" in output

    async def test_add_server_should_add_server_successfully(self, cli, capsys):
        """
        验收标准：用户通过 /server add <name> <url> 成功添加服务器后，服务器列表中应包含该服务器
        """
        output = await run_cli_with_inputs(
            cli,
            capsys,
            [
                "/server add test http://localhost:8000",
                "/server list",
                "/exit",
            ],
        )
        assert "test" in output
        assert "http://localhost:8000" in output

    async def test_add_server_with_duplicate_name_should_fail(self, cli, capsys):
        """
        验收标准：如果添加的服务器名称已存在，则应提示名称重复，不能添加
        """
        output = await run_cli_with_inputs(
            cli,
            capsys,
            [
                "/server add test http://localhost:8000",
                "/server add test http://localhost:9000",
                "/exit",
            ],
        )
        assert "名称重复" in output or "already exists" in output

    async def test_one_server_configured_should_reply_which_server(self, cli, capsys):
        """
        验收标准：如果配置了一个服务器，则回答配置的服务器是什么
        """
        output = await run_cli_with_inputs(
            cli,
            capsys,
            [
                "/server add test http://localhost:8000",
                "/clear",
                "/server list",
                "/exit",
            ],
        )
        assert "test" in output
        assert "http://localhost:8000" in output

    async def test_multiple_servers_configured_should_list_all_servers(
        self, cli, capsys
    ):
        """
        验收标准：如果配置了多个服务器，则列出所有可用的服务器
        """
        output = await run_cli_with_inputs(
            cli,
            capsys,
            [
                "/server add test1 http://localhost:8000",
                "/server add test2 http://localhost:9000",
                "/server list",
                "/exit",
            ],
        )
        assert "test1" in output
        assert "test2" in output
        assert "http://localhost:8000" in output
        assert "http://localhost:9000" in output

    async def test_remove_server_should_remove_server_successfully(self, cli, capsys):
        """
        验收标准：用户通过 /server remove <name> 成功删除服务器后，服务器列表中不应再包含该服务器
        """
        output = await run_cli_with_inputs(
            cli,
            capsys,
            [
                "/server add test http://localhost:1000",
                "/server remove test",
                "/clear",
                "/server list",
                "/exit",
            ],
        )
        # 提取“服务器列表”部分
        if "服务器列表：" in output:
            assert "test" not in output
        else:
            # 如果没有服务器列表，说明已被正确删除
            assert "没有服务器可用" in output

    async def test_remove_nonexistent_server_should_reply_no_such_server(
        self, cli, capsys
    ):
        """
        验收标准：删除不存在的服务器时，应提示没有这样的服务器
        """
        output = await run_cli_with_inputs(
            cli,
            capsys,
            [
                "/server remove notfound",
                "/exit",
            ],
        )
        assert "没有这样的服务器" in output or "No such server" in output

    async def test_edit_server_should_update_server_url(self, cli, capsys):
        """
        验收标准：用户通过 /server edit <name> <url> 修改服务器地址后，服务器信息应被正确更新
        """
        output = await run_cli_with_inputs(
            cli,
            capsys,
            [
                "/server add test http://localhost:8000",
                "/server edit test http://localhost:9000",
                "/server info test",
                "/exit",
            ],
        )
        assert "http://localhost:8000" not in output
        assert "http://localhost:9000" in output

    async def test_info_server_should_show_server_details(self, cli, capsys):
        """
        验收标准：用户通过 /server info <name> 能正确显示服务器的详细信息
        """
        output = await run_cli_with_inputs(
            cli,
            capsys,
            [
                "/server add test http://localhost:8000",
                "/server info test",
                "/exit",
            ],
        )
        assert "test" in output
        assert "http://localhost:8000" in output


# 功能点2：用户指定 MCP 服务器回答问题
@pytest.mark.tbd
class TestUserSpecifyServerToAnswer:
    """
    功能点名称：用户指定 MCP 服务器回答问题
    操作流程：配置了服务器，用户指定服务器回答问题，回答用户问题
    """

    def test_server_not_exist_should_reply_no_such_server(self):
        """
        验收标准：当服务器不存在时要回答没有这样的服务器
        """
        pass

    def test_server_unreachable_should_reply_server_unreachable(self):
        """
        验收标准：当服务器连接不上时要回答服务器无法连接
        """
        pass

    def test_server_cannot_help_should_reply_no_relevant_info(self):
        """
        验收标准：当服务器对回答问题没有帮助时，回答服务器不能提供问题相关的信息
        """
        pass

    def test_using_server_should_show_using_server(self):
        """
        验收标准：使用服务器过程中，要显示出正在使用服务器
        """
        pass

    def test_specify_server_should_route_question_to_server(self):
        """
        验收标准：用户在对话中通过指定服务器（如 @服务器名 问题）时，系统应将问题路由到对应服务器
        """
        pass


# 功能点3：自主决定使用服务器
@pytest.mark.tbd
class TestAutoDecideUseServer:
    """
    功能点名称：自主决定使用服务器
    操作流程：前置条件：用户配置了服务器，用户问问题，回答用户问题
    """

    def test_question_suitable_for_service_should_use_service(self):
        """
        验收标准：当用户的问题适合用服务解答时，系统应该用服务来获取信息比回答问题
        """
        pass

    def test_question_not_need_server_should_answer_directly(self):
        """
        验收标准：当用户的问题不需要服务器就可以直接回答时，应该直接回答
        """
        pass

    def test_server_no_valid_response_should_not_use(self):
        """
        验收标准：如果适合服务器工具辅助回答，但服务器未给出有效响应，则不采用
        """
        pass
