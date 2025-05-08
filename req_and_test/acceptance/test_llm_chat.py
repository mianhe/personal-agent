import sys
from io import StringIO
from unittest.mock import patch, AsyncMock

import pytest


@pytest.mark.asyncio
async def test_show_processing_indicator(cli):
    """测试显示处理指示器"""
    with patch(
        "prompt_toolkit.PromptSession.prompt_async", new_callable=AsyncMock
    ) as mock_prompt:
        mock_prompt.side_effect = ["Hello", "/exit"]
        with StringIO() as stdout:
            sys.stdout = stdout
            await cli.start()
            output = stdout.getvalue()
            assert "Thinking..." in output


@pytest.mark.asyncio
async def test_maintain_conversation_context(cli):
    """测试维护对话上下文"""
    with patch(
        "prompt_toolkit.PromptSession.prompt_async", new_callable=AsyncMock
    ) as mock_prompt:
        mock_prompt.side_effect = [
            "What is 1+1?",
            "What was my previous question?",
            "/exit",
        ]
        with StringIO() as stdout:
            sys.stdout = stdout
            await cli.start()
            output = stdout.getvalue()
            assert "1+1" in output


@pytest.mark.asyncio
async def test_handle_network_error(cli):
    """测试处理网络错误"""
    with patch(
        "prompt_toolkit.PromptSession.prompt_async", new_callable=AsyncMock
    ) as mock_prompt:
        mock_prompt.side_effect = ["Hello", "/exit"]
        with patch("litellm.completion", side_effect=ConnectionError("Network error")):
            with StringIO() as stdout:
                sys.stdout = stdout
                await cli.start()
                output = stdout.getvalue()
                assert "Error" in output
