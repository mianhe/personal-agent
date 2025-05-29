from typing import List, Dict, Optional
from .api.server_registry import ServerRegistry


class MemoryServerRegistry(ServerRegistry):
    """
    基于内存的MCP服务器注册与管理实现。
    """

    def __init__(self):
        self._servers: Dict[str, str] = {}

    def list_servers(self) -> List[Dict[str, str]]:
        """
        获取所有已注册的服务器信息。
        """
        return [{"name": name, "url": url} for name, url in self._servers.items()]

    def add_server(self, name: str, url: str) -> bool:
        """
        添加新服务器。
        """
        if name in self._servers:
            return False
        self._servers[name] = url
        return True

    def remove_server(self, name: str) -> bool:
        """
        删除指定名称的服务器。
        """
        if name not in self._servers:
            return False
        del self._servers[name]
        return True

    def get_server(self, name: str) -> Optional[Dict[str, str]]:
        """
        获取指定名称服务器的详细信息。
        """
        if name not in self._servers:
            return None
        return {"name": name, "url": self._servers[name]}

    def edit_server(self, name: str, url: str) -> bool:
        """
        修改指定服务器的地址。
        """
        if name not in self._servers:
            return False
        self._servers[name] = url
        return True
