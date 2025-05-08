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

            # 设置 provider
            if self.config.llm.provider == "deepseek":
                litellm.api_base = "https://api.deepseek.com/v1"
        except Exception as e:
            print(f"Error initializing chat service: {e}")
            raise

    async def send_message(self, message: str) -> str:
        """发送消息并获取回复"""
        try:
            # 准备消息列表
            messages = [{"role": "user", "content": message}]
            if self._context:
                messages = self._context + messages

            # 调用 LLM
            response = litellm.completion(
                model=self.config.llm.model,
                messages=messages,
                temperature=self.config.llm.parameters.temperature,
                max_tokens=self.config.llm.parameters.max_tokens,
                api_key=self.config.llm.api_key,
            )

            # 获取回复内容
            response_text = response.choices[0].message.content

            # 更新上下文
            self._context.extend(
                [
                    {"role": "user", "content": message},
                    {"role": "assistant", "content": response_text},
                ]
            )

            return response_text

        except Exception as e:
            raise ConnectionError(f"Failed to send message: {e}")

    def get_context(self) -> List[Dict[str, str]]:
        """获取当前对话上下文"""
        return self._context

    def clear_context(self) -> None:
        """清除当前对话上下文"""
        self._context = []
