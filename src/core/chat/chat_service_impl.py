from typing import List, Dict, Optional
from core.chat.chat_service_api import ChatService
from config.config import Config, LLMConfig

# langchain 0.3.x 推荐用法
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI


class ChatServiceImpl(ChatService):
    """使用 langchain 实现的 LLM 聊天服务，支持 OpenAI 兼容 API（如 deepseek、qwen）"""

    def __init__(self, config: Optional[Config] = None):
        try:
            self.config = config or Config.load_config()
            self._context: List[Dict[str, str]] = []
            self.llm: BaseChatModel = self._init_llm()
        except Exception as e:
            print(f"Error initializing chat service: {e}")
            raise

    def _init_llm(self) -> BaseChatModel:
        model = self.config.llm.model
        api_key = self.config.llm.api_key
        api_base = self.config.llm.api_base
        temperature = self.config.llm.parameters.temperature
        max_tokens = self.config.llm.parameters.max_tokens

        # 统一用 OpenAI 兼容 API
        return ChatOpenAI(
            model=model,
            api_key=api_key,
            base_url=api_base,
            temperature=temperature,
            max_tokens=max_tokens,
        )

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
            messages = []
            for msg in self._context:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))
            messages.append(HumanMessage(content=message))

            # 调用 LLM 服务
            reply_msg = await self.llm.ainvoke(messages)
            reply = (
                reply_msg.content if hasattr(reply_msg, "content") else str(reply_msg)
            )

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
