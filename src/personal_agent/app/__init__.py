"""
负责系统的启动、初始化和生命周期管理，是各个子系统的容器和协调者
"""

from .container import AppContainer as Container

__all__ = ["Container"]
