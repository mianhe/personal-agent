from abc import ABC, abstractmethod
from typing import List, Dict
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI


class LLMAdapter(ABC):
    @abstractmethod
    async def chat(self, messages: List[Dict[str, str]]) -> str:
        """发送消息列表，返回回复内容"""


class OpenAICompatibleLLMAdapter(LLMAdapter):
    def __init__(self, llm_config):
        self.llm = self._init_llm(llm_config)

    def _init_llm(self, config) -> BaseChatModel:
        return ChatOpenAI(
            model=config.model,
            api_key=config.api_key,
            base_url=config.api_base,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
        )

    async def chat(self, messages: List[Dict[str, str]]) -> str:
        # 将通用消息格式转为 langchain 消息对象
        lc_messages = []
        for msg in messages:
            if msg["role"] == "user":
                lc_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                lc_messages.append(AIMessage(content=msg["content"]))
        # 调用 LLM
        reply_msg = await self.llm.ainvoke(lc_messages)
        return reply_msg.content if hasattr(reply_msg, "content") else str(reply_msg)
