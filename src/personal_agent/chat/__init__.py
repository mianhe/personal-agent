"""
chat 子系统职责：负责与LLM模型交互，处理用户输入，并返回响应。
"""

from .api.chat_service import ChatService
from .container import Container

__all__ = ["ChatService", "Container"]
