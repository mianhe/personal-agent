"""测试配置。"""


def pytest_configure(config):
    """注册自定义标记"""
    config.addinivalue_line("markers", "implemented: 标记已实现的测试用例")
    config.addinivalue_line("markers", "tbd: 标记待实现的测试用例")
    config.addinivalue_line("markers", "dev_ongoing: 标记正在实现中的测试")
    config.addinivalue_line("markers", "smoke: 标记需要加入 smoke test 的测试")
