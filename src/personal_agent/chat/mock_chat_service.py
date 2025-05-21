from typing import List, Dict
from .api.chat_service_api import ChatService


class MockChatService(ChatService):
    """Mock implementation of ChatService for testing and development purposes."""

    def __init__(self):
        self._context: List[Dict[str, str]] = []
        self._connected = False

    async def connect(self) -> bool:
        """Mock connection to LLM service."""
        self._connected = True
        return True

    async def disconnect(self) -> None:
        """Mock disconnection from LLM service."""
        self._connected = False

    async def send_message(self, message: str) -> str:
        """Mock sending a message and getting a response."""
        if not self._connected:
            raise ConnectionError("Not connected to LLM service")

        # 添加用户消息到上下文
        self._context.append({"role": "user", "content": message})

        # 生成模拟回复
        mock_response = f"This is a mock response to: {message}"

        # 添加助手回复到上下文
        self._context.append({"role": "assistant", "content": mock_response})

        return mock_response

    def get_context(self) -> List[Dict[str, str]]:
        """Get the mock conversation context."""
        return self._context

    def clear_context(self) -> None:
        """Clear the mock conversation context."""
        self._context = []
