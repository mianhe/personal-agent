"""
负责提供配置信息，包括LLM模型配置、服务器配置等。
"""

from .api.config_api import ConfigSupplier
from .container import ConfigContainer

__all__ = ["ConfigSupplier", "ConfigContainer"]
