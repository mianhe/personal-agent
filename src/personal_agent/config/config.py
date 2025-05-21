from pathlib import Path
from typing import Optional
import yaml
from pydantic import BaseModel, Field
from .api.config_api import ConfigSupplier


class FileConfigSupplier(ConfigSupplier):
    def __init__(self, config_path: Optional[Path] = None):
        self._config = OverallConfig.load_config(config_path)

    def get_llm_config(self):
        return self._config.llm

    def get_app_config(self):
        return self._config.app

    def get_cli_config(self):
        return self._config.cli


class LLMConfig(BaseModel):
    """LLM 配置"""

    provider: str
    model: str
    api_key: str
    api_base: Optional[str] = None  # API 基础 URL，如果为 None 则使用默认值
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(default=1000, gt=0)
    timeout: int = Field(default=30, gt=0)
    retry_attempts: int = Field(default=3, ge=0)


class CLIConfig(BaseModel):
    """CLI 配置"""

    prompt: str = "> "
    welcome_message: str = "Welcome to Personal Agent CLI ..."


class SystemConfig(BaseModel):
    """应用配置"""

    name: str
    version: str
    environment: str


class OverallConfig(BaseModel):
    """总配置"""

    llm: LLMConfig
    app: SystemConfig

    @classmethod
    def load_config(cls, config_path: Optional[Path] = None) -> "OverallConfig":
        """加载配置文件

        Args:
            config_path: 配置文件路径，如果为 None 则使用默认路径

        Returns:
            Config: 配置对象
        """
        if config_path is None:
            config_path = Path.cwd() / "config" / "config.yaml"

        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)

        return cls(**config_data)
