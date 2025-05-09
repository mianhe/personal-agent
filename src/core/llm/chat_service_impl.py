from typing import List, Dict, Optional
import litellm
from litellm import completion

from ..api.chat_service import ChatService
from .config import Config, LLMConfig


class ChatServiceImpl(ChatService):
    """使用 litellm 实现的 LLM 聊天服务"""

    def __init__(self, config: Optional[Config] = None):
        try:
            self.config = config or Config.load_config()
            self._context: List[Dict[str, str]] = []

            # 配置 litellm
            litellm.verbose = False
            litellm.timeout = self.config.llm.connection.timeout

            # 设置 API base
            if self.config.llm.api_base:
                litellm.api_base = self.config.llm.api_base
        except Exception as e:
            print(f"Error initializing chat service: {e}")
            raise

    async def send_message(self, message: str) -> str:
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
            messages = self._context + [{"role": "user", "content": message}]

            # 调用 LLM 服务
            response = await litellm.acompletion(
                model=self.config.llm.model,
                messages=messages,
                temperature=self.config.llm.parameters.temperature,
                max_tokens=self.config.llm.parameters.max_tokens,
                api_key=self.config.llm.api_key,
                custom_llm_provider=self.config.llm.provider,
            )

            # 获取回复内容
            reply = response.choices[0].message.content

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
