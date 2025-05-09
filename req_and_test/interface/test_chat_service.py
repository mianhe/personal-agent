from unittest.mock import patch, MagicMock, AsyncMock
import pytest
from core.llm.chat_service_impl import ChatServiceImpl
from core.llm.config import Config, LLMConfig, AppConfig


@pytest.fixture(scope="function")
def mock_litellm():
    """模拟 litellm 服务"""
    with patch("litellm.acompletion", new_callable=AsyncMock) as mock:
        mock.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="这是一个测试回复"))]
        )
        yield mock


class TestSendMessage:
    """测试发送消息实现"""

    @pytest.fixture
    def chat_service(self):
        """创建 ChatServiceImpl 实例"""
        config = Config(
            llm=LLMConfig(
                provider="deepseek",
                model="deepseek-chat",
                api_key="test_key",
                connection={"timeout": 30},
                parameters={"temperature": 0.7, "max_tokens": 1000},
            ),
            app=AppConfig(name="test-app", version="0.1.0", environment="test"),
        )
        return ChatServiceImpl(config)

    @pytest.mark.asyncio
    async def test_send_message_should_update_context_and_return_response(
        self, chat_service, mock_litellm
    ):
        """测试发送消息应该更新上下文并返回响应"""
        # 发送第一条消息
        message = "你好"
        response = await chat_service.send_message(message)

        # 验证响应
        assert response == "这是一个测试回复"
        mock_litellm.assert_called_once()

        # 验证 litellm 调用参数
        call_args = mock_litellm.call_args[1]
        assert call_args["model"] == "deepseek-chat"
        assert call_args["temperature"] == 0.7
        assert call_args["max_tokens"] == 1000
        assert call_args["api_key"] == "test_key"

        # 验证消息列表包含用户消息
        messages = call_args["messages"]
        assert len(messages) == 1  # 调用时只有用户消息
        assert messages[0]["role"] == "user"
        assert messages[0]["content"] == "你好"

        # 验证上下文包含完整对话
        context = chat_service.get_context()
        assert len(context) == 2  # 用户消息 + 助手回复
        assert context[0]["role"] == "user"
        assert context[0]["content"] == "你好"
        assert context[1]["role"] == "assistant"
        assert context[1]["content"] == "这是一个测试回复"

        # 发送第二条消息，验证上下文传递
        mock_litellm.reset_mock()
        response = await chat_service.send_message("第二条消息")

        # 验证第二次调用的消息列表包含完整上下文
        call_args = mock_litellm.call_args[1]
        messages = call_args["messages"]
        assert len(messages) == 3  # 第一条用户消息 + 助手回复 + 第二条用户消息
        assert messages[0]["role"] == "user"
        assert messages[0]["content"] == "你好"
        assert messages[1]["role"] == "assistant"
        assert messages[1]["content"] == "这是一个测试回复"
        assert messages[2]["role"] == "user"
        assert messages[2]["content"] == "第二条消息"

    @pytest.mark.asyncio
    async def test_litellm_error_should_raise_connection_error(
        self, chat_service, mock_litellm
    ):
        """测试 litellm 调用失败应该抛出连接错误"""
        mock_litellm.side_effect = Exception("API Error")
        with pytest.raises(ConnectionError):
            await chat_service.send_message("你好")


class TestGetContext:
    """测试获取上下文实现"""

    @pytest.fixture
    def chat_service(self):
        """创建 ChatServiceImpl 实例"""
        config = Config(
            llm=LLMConfig(
                provider="deepseek",
                model="deepseek-chat",
                api_key="test_key",
                connection={"timeout": 30},
                parameters={"temperature": 0.7, "max_tokens": 1000},
            ),
            app=AppConfig(name="test-app", version="0.1.0", environment="test"),
        )
        return ChatServiceImpl(config)

    @pytest.mark.asyncio
    async def test_get_context_should_return_expected_history(
        self, chat_service, mock_litellm  # pylint: disable=unused-argument
    ):
        """测试获取上下文应该返回预期的对话历史"""
        # 发送消息建立上下文
        await chat_service.send_message("你好")

        context = chat_service.get_context()
        assert len(context) == 2  # 用户消息 + 助手回复
        assert context[0]["role"] == "user"
        assert context[0]["content"] == "你好"
        assert context[1]["role"] == "assistant"
        assert context[1]["content"] == "这是一个测试回复"


class TestClearContext:
    """测试清除上下文实现"""

    @pytest.fixture
    def chat_service(self):
        """创建 ChatServiceImpl 实例"""
        config = Config(
            llm=LLMConfig(
                provider="deepseek",
                model="deepseek-chat",
                api_key="test_key",
                connection={"timeout": 30},
                parameters={"temperature": 0.7, "max_tokens": 1000},
            ),
            app=AppConfig(name="test-app", version="0.1.0", environment="test"),
        )
        return ChatServiceImpl(config)

    @pytest.mark.asyncio
    async def test_clear_context_should_empty_history(
        self, chat_service, mock_litellm  # pylint: disable=unused-argument
    ):
        """测试清除上下文应该清空对话历史"""
        # 先建立一些上下文
        await chat_service.send_message("你好")
        assert len(chat_service.get_context()) > 0

        # 清除上下文
        chat_service.clear_context()
        assert len(chat_service.get_context()) == 0
