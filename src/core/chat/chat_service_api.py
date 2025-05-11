from abc import ABC, abstractmethod
from typing import List, Dict


class ChatService(ABC):
    """聊天服务接口

    定义了聊天服务的基本功能，包括消息发送和上下文管理。
    """

    @abstractmethod
    async def send_message(self, message: str) -> str:
        """发送消息并获取回复

        Args:
            message: 要发送的消息

        Returns:
            str: 服务的回复

        Raises:
            ConnectionError: 连接错误
            ServiceError: 服务错误
        """
        pass

    @abstractmethod
    def get_context(self) -> List[Dict[str, str]]:
        """获取当前对话上下文

        Returns:
            List[Dict[str, str]]: 对话历史，每个消息包含 role 和 content
        """
        pass

    @abstractmethod
    def clear_context(self) -> None:
        """清除当前对话上下文"""
        pass
