from typing import List, Dict
from .api.chat_service_api import ChatService
from .llm_adapter import LLMAdapter


class ChatServiceImpl(ChatService):
    """使用 langchain 实现的 LLM 聊天服务，支持 OpenAI 兼容 API（如 deepseek、qwen）"""

    def __init__(self, llm_adapter: LLMAdapter):
        self.llm_adapter = llm_adapter
        self._context: List[Dict[str, str]] = []

    async def get_response(self, message: str) -> str:
        """发送消息到 LLM 服务

        Args:
            message: 用户消息
        Returns:
            str: LLM 的回复
        Raises:
            ConnectionError: 连接失败时抛出
        """
        try:
            # 构建消息列表，包含历史上下文
            messages = self._context.copy()
            messages.append({"role": "user", "content": message})

            # 调用 LLM Adapter
            reply = await self.llm_adapter.chat(messages)

            # 更新上下文
            self._context.append({"role": "user", "content": message})
            self._context.append({"role": "assistant", "content": reply})

            return reply
        except Exception as e:
            raise ConnectionError(f"Failed to send message: {e}") from e

    def get_context(self) -> List[Dict[str, str]]:
        """获取当前对话上下文"""
        return self._context

    def clear_context(self) -> None:
        """清除当前对话上下文"""
        self._context = []
