# pylint: disable=no-member

from unittest.mock import AsyncMock
import pytest
from dependency_injector import providers
from personal_agent.container import AppContainer  # 使用顶层容器

pytestmark = pytest.mark.smoke


@pytest.fixture
def app_container():
    # 这里可以用 FileConfigProvider() 或 mock config_provider
    container = AppContainer()
    yield container
    container.unwire()


@pytest.fixture
def mock_adapter():
    mock = AsyncMock()
    mock.chat.return_value = "这是一个测试回复"
    return mock


@pytest.fixture
def chat_service(app_container, mock_adapter):
    app_container.chat_container().llm_adapter.override(providers.Object(mock_adapter))
    return app_container.chat_container().chat_service()


class TestGetResponse:
    """测试发送消息实现"""

    @pytest.mark.asyncio
    async def test_get_response_should_update_context_and_return_response(
        self, chat_service, mock_adapter
    ):
        """测试发送消息应该更新上下文并返回响应"""
        message = "你好"
        response = await chat_service.get_response(message)
        assert response == "这是一个测试回复"
        mock_adapter.chat.assert_called_once()
        context = chat_service.get_context()
        assert len(context) == 2  # 用户消息 + 助手回复
        assert context[0]["role"] == "user"
        assert context[0]["content"] == "你好"
        assert context[1]["role"] == "assistant"
        assert context[1]["content"] == "这是一个测试回复"
        mock_adapter.chat.reset_mock()
        response = await chat_service.get_response("第二条消息")
        mock_adapter.chat.assert_called_once()

    @pytest.mark.asyncio
    async def test_llm_error_should_raise_connection_error(
        self, chat_service, mock_adapter
    ):
        """测试 LLM 调用失败应该抛出连接错误"""
        mock_adapter.chat.side_effect = Exception("API Error")
        with pytest.raises(ConnectionError):
            await chat_service.get_response("你好")


class TestGetContext:
    """测试获取上下文实现"""

    @pytest.mark.asyncio
    async def test_get_context_should_return_expected_history(
        self, chat_service, mock_adapter  # pylint: disable=unused-argument
    ):
        """测试获取上下文应该返回预期的对话历史"""
        # 发送消息建立上下文
        await chat_service.get_response("你好")

        context = chat_service.get_context()
        assert len(context) == 2  # 用户消息 + 助手回复
        assert context[0]["role"] == "user"
        assert context[0]["content"] == "你好"
        assert context[1]["role"] == "assistant"
        assert context[1]["content"] == "这是一个测试回复"


class TestClearContext:
    """测试清除上下文实现"""

    @pytest.mark.asyncio
    async def test_clear_context_should_empty_history(
        self, chat_service, mock_adapter  # pylint: disable=unused-argument
    ):
        """测试清除上下文应该清空对话历史"""
        # 先建立一些上下文
        await chat_service.get_response("你好")
        assert len(chat_service.get_context()) > 0

        # 清除上下文
        chat_service.clear_context()
        assert len(chat_service.get_context()) == 0
