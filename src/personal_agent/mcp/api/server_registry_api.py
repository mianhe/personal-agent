from abc import ABC, abstractmethod
from typing import List, Optional, Dict


class ServerRegistry(ABC):
    """
    MCP服务器注册与管理接口，负责服务器的增删查改。
    """

    @abstractmethod
    def list_servers(self) -> List[Dict[str, str]]:
        """
        获取所有已注册的服务器信息。

        Returns:
            List[Dict[str, str]]: 服务器列表，每个元素包含 'name' 和 'url' 字段。
        """

    @abstractmethod
    def add_server(self, name: str, url: str) -> bool:
        """
        添加新服务器。

        Args:
            name (str): 服务器名称，唯一。
            url (str): 服务器地址。

        Returns:
            bool: 添加成功返回 True，若名称重复返回 False。
        """

    @abstractmethod
    def remove_server(self, name: str) -> bool:
        """
        删除指定名称的服务器。

        Args:
            name (str): 服务器名称。

        Returns:
            bool: 删除成功返回 True，若不存在返回 False。
        """

    @abstractmethod
    def get_server(self, name: str) -> Optional[Dict[str, str]]:
        """
        获取指定名称服务器的详细信息。

        Args:
            name (str): 服务器名称。

        Returns:
            Optional[Dict[str, str]]: 服务器信息，若不存在返回 None。
        """

    @abstractmethod
    def edit_server(self, name: str, url: str) -> bool:
        """
        修改指定服务器的地址。

        Args:
            name (str): 服务器名称。
            url (str): 新的服务器地址。

        Returns:
            bool: 修改成功返回 True，若不存在返回 False。
        """
