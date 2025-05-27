from urllib.parse import urlparse
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from icontract import require, ensure


def is_valid_url(url: str) -> bool:
    if not isinstance(url, str) or not url:
        return False
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


class ServerRegistry(ABC):
    """
    MCP服务器注册与管理接口，负责服务器的增删查改。
    """

    @abstractmethod
    @ensure(lambda result: isinstance(result, list))
    def list_servers(self) -> List[Dict[str, str]]:
        """
        获取所有已注册的服务器信息。
        """

    @abstractmethod
    @require(
        lambda name: isinstance(name, str) and name != "", "服务器名称必须为非空字符串"
    )
    @require(is_valid_url, "服务器地址必须为合法的 URL")
    @ensure(lambda result: isinstance(result, bool))
    def add_server(self, name: str, url: str) -> bool:
        """
        添加新服务器。若名称重复则添加失败。
        """

    @abstractmethod
    @require(
        lambda name: isinstance(name, str) and name != "", "服务器名称必须为非空字符串"
    )
    @ensure(lambda result: isinstance(result, bool))
    def remove_server(self, name: str) -> bool:
        """
        删除指定名称的服务器。
        若服务器不存在则删除失败。
        """

    @abstractmethod
    @require(
        lambda name: isinstance(name, str) and name != "", "服务器名称必须为非空字符串"
    )
    @ensure(
        lambda result: result is None
        or (isinstance(result, dict) and "name" in result and "url" in result)
    )
    def get_server(self, name: str) -> Optional[Dict[str, str]]:
        """
        获取指定名称服务器的详细信息。
        若不存在则返回 None。
        """

    @abstractmethod
    @require(
        lambda name: isinstance(name, str) and name != "", "服务器名称必须为非空字符串"
    )
    @require(is_valid_url, "服务器地址必须为合法的 URL")
    @ensure(lambda result: isinstance(result, bool))
    def edit_server(self, name: str, url: str) -> bool:
        """
        修改指定服务器的地址。
        若服务器不存在则修改失败。
        """
