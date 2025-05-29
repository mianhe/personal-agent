from unittest.mock import AsyncMock
import pytest
from personal_agent.chat import Container as ChatContainer
from personal_agent.chat import ChatService


class TestChatServiceApi:
    mock_llm_adapter: AsyncMock
    service: ChatService

    @pytest.fixture(autouse=True)
    def setup_service(self):
        # mock llm_adapter
        self.mock_llm_adapter = AsyncMock()

        async def mock_chat(message):
            return f"mocked response to {message}"

        self.mock_llm_adapter.chat.side_effect = mock_chat

        container = ChatContainer(
            configer=lambda: None, llm_adapter=self.mock_llm_adapter
        )
        self.service = container.chat_service()

    @pytest.mark.asyncio
    async def test_get_response_should_return_mocked(self):
        reply = await self.service.get_response("hello")
        assert reply == "mocked response to [{'role': 'user', 'content': 'hello'}]"
        self.mock_llm_adapter.chat.assert_called_once()

    @pytest.mark.asyncio
    async def test_context_should_update_and_clear(self):
        # 初始上下文为空
        assert self.service.get_context() == []
        # 模拟添加上下文
        reply = await self.service.get_response("hi")

        assert self.service.get_context() == [
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": reply},
        ]
        # 清除上下文
        self.service.clear_context()
        assert self.service.get_context() == []
