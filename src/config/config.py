from pathlib import Path
from typing import Optional
import yaml
from pydantic import BaseModel, Field


class LLMParameters(BaseModel):
    """LLM 参数配置"""

    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(default=1000, gt=0)


class ConnectionConfig(BaseModel):
    """连接配置"""

    timeout: int = Field(default=30, gt=0)
    retry_attempts: int = Field(default=3, ge=0)


class LLMConfig(BaseModel):
    """LLM 配置"""

    provider: str
    model: str
    api_key: str
    api_base: Optional[str] = None  # API 基础 URL，如果为 None 则使用默认值
    parameters: LLMParameters = Field(default_factory=LLMParameters)
    connection: ConnectionConfig = Field(default_factory=ConnectionConfig)


class CLIConfig(BaseModel):
    """CLI 配置"""

    prompt: str = "> "
    welcome_message: str = "Welcome to Personal Agent CLI!"


class AppConfig(BaseModel):
    """应用配置"""

    name: str
    version: str
    environment: str
    cli: CLIConfig = Field(default_factory=CLIConfig)


class Config(BaseModel):
    """总配置"""

    llm: LLMConfig
    app: AppConfig

    @classmethod
    def load_config(cls, config_path: Optional[Path] = None) -> "Config":
        """加载配置文件

        Args:
            config_path: 配置文件路径，如果为 None 则使用默认路径

        Returns:
            Config: 配置对象
        """
        if config_path is None:
            # 获取当前文件所在目录
            current_dir = Path(__file__).parent.parent.parent
            config_path = current_dir / "config" / "config.yaml"

        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)

        return cls(**config_data)
