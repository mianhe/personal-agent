from typing import Any, List
from abc import ABC, abstractmethod
from core.mcp.types import ToolDescription


class MCPClient(ABC):
    """
    MCP 客户端主接口，仅供 LLM 调用。
    提供能力发现、工具调用、能力缓存刷新等方法。
    """

    @abstractmethod
    async def list_tools(self) -> List[ToolDescription]:
        """
        获取所有聚合后的工具能力描述
        返回: List[ToolDescription]
        """
        pass

    @abstractmethod
    async def call_tool(self, tool_name: str, params: dict) -> Any:
        """
        调用指定工具，自动路由到对应 MCPServer
        参数:
            tool_name: 工具名（可带 server 前缀）
            params: 工具调用参数
        返回: 工具调用结果（ToolOutput）
        """
        pass

    @abstractmethod
    async def refresh_tools(self) -> None:
        """
        主动刷新能力缓存
        """
        pass
