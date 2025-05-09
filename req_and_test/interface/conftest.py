import os
import pytest


def pytest_collection_modifyitems(items):
    """为 interface 目录下的所有测试添加 smoke 标记"""
    # 获取当前 conftest.py 所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    for item in items:
        # 获取测试文件的实际路径
        test_file = os.path.abspath(item.fspath)
        # 如果测试文件在当前目录或其子目录中
        if test_file.startswith(current_dir):
            item.add_marker(pytest.mark.smoke)
