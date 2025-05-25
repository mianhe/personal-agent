# pylint: disable=no-member

"""共享的测试夹具。"""

import pytest

from personal_agent.app.container import AppContainer


@pytest.fixture
def cli():
    """提供CLI实例"""
    cli = AppContainer().cli_container.cli()
    return cli
