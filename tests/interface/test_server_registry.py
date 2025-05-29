import pytest
from personal_agent.mcp import Container as MCPContainer
from personal_agent.mcp import ServerRegistry


class TestServerRegistry:

    registry: ServerRegistry

    @pytest.fixture(autouse=True)
    def setup_registry(self):
        container = MCPContainer()
        self.registry = container.server_registry()

    def test_add_server_should_succeed(self):
        result = self.registry.add_server("server1", "http://localhost:8000")
        assert result is True
        servers = self.registry.list_servers()
        assert any(
            s["name"] == "server1" and s["url"] == "http://localhost:8000"
            for s in servers
        )

    def test_add_server_with_duplicate_name_should_fail(self):
        self.registry.add_server("server1", "http://localhost:8000")
        result = self.registry.add_server("server1", "http://localhost:9000")
        assert result is False
        servers = self.registry.list_servers()
        assert len([s for s in servers if s["name"] == "server1"]) == 1

    def test_remove_server_should_succeed(self):
        self.registry.add_server("server1", "http://localhost:8000")
        result = self.registry.remove_server("server1")
        assert result is True
        assert self.registry.get_server("server1") is None

    def test_remove_nonexistent_server_should_fail(self):
        result = self.registry.remove_server("not_exist")
        assert result is False

    def test_get_server_should_return_correct_info(self):
        self.registry.add_server("server1", "http://localhost:8000")
        info = self.registry.get_server("server1")
        assert info == {"name": "server1", "url": "http://localhost:8000"}

    def test_get_server_nonexistent_should_return_none(self):
        info = self.registry.get_server("not_exist")
        assert info is None

    def test_edit_server_should_succeed(self):
        self.registry.add_server("server1", "http://localhost:8000")
        result = self.registry.edit_server("server1", "http://localhost:9000")
        assert result is True
        info = self.registry.get_server("server1")
        assert info["url"] == "http://localhost:9000"

    def test_edit_server_nonexistent_should_fail(self):
        result = self.registry.edit_server("not_exist", "http://localhost:9000")
        assert result is False
