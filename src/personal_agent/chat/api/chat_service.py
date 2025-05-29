from abc import ABC, abstractmethod
from typing import List, Dict
from icontract import require, ensure


class ChatService(ABC):
    """
    聊天服务接口

    该接口定义了标准的聊天服务能力，包括消息交互、会话上下文的获取与管理。
    实现类应确保异常处理和上下文一致性，适用于多种聊天后端（如本地模型、云服务等）。
    """

    @abstractmethod
    @require(
        lambda message: isinstance(message, str) and message.strip() != "",
        "消息内容必须为非空字符串",
    )
    @ensure(
        lambda result: isinstance(result, str) and result.strip() != "",
        "回复内容必须为非空字符串",
    )
    async def get_response(self, message: str) -> str:
        """
        发送一条用户消息，并异步获取聊天服务的回复。

        参数:
            message (str): 用户输入的消息内容，不能为空字符串。

        返回:
            str: 聊天服务生成的回复内容，不能为空字符串。

        异常:
            ConnectionError: 无法连接到聊天服务时抛出。

        说明:
            该方法应保证线程安全（如适用），并在异常情况下提供明确的错误信息。
        """

    @abstractmethod
    @ensure(lambda result: isinstance(result, list), "返回值必须为列表")
    @ensure(
        lambda result: all(
            isinstance(item, dict) and "role" in item and "content" in item
            for item in result
        ),
        "每个历史项必须包含 role 和 content 字段",
    )
    def get_context(self) -> List[Dict[str, str]]:
        """
        获取当前会话的完整上下文历史。

        返回:
            List[Dict[str, str]]: 对话历史列表。每个元素为字典，包含：
                - role (str): 消息发送方角色（如 'user', 'assistant'）。
                - content (str): 消息内容。

        说明:
            返回的历史应按时间顺序排列，便于重现完整对话。
        """

    @abstractmethod
    @ensure(lambda result: result is None, "无返回值")
    def clear_context(self) -> None:
        """
        清空当前会话的上下文历史。

        说明:
            调用后，get_context() 应返回空列表，后续对话视为新会话。
        """
