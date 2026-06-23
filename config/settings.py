from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pathlib import Path


class Settings(BaseSettings):
    # -------------------------------------------------------------------------
    # 基础应用配置
    # -------------------------------------------------------------------------
    APP_NAME: str = "智能研发 Agent 协作平台"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # -------------------------------------------------------------------------
    # 数据库配置 (MySQL)
    # -------------------------------------------------------------------------
    DB_HOST: str = "localhost"
    DB_PORT: int = 3307
    DB_USER: str = "root"
    DB_PASSWORD: str = "123456"
    DB_NAME: str = "agent_platform"

    @property
    def DATABASE_URL(self) -> str:
        return f"sqlite:///{self.DATA_DIR}/{self.DB_NAME}.db"

    # -------------------------------------------------------------------------
    # 向量数据库配置 (Qdrant)
    # -------------------------------------------------------------------------
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_COLLECTION_NAME: str = "agent_memory"

    # -------------------------------------------------------------------------
    # 缓存配置 (Redis)
    # -------------------------------------------------------------------------
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    REDIS_CACHE_TTL: int = 3600

    # -------------------------------------------------------------------------
    # LLM 配置 (DeepSeek)
    # -------------------------------------------------------------------------
    LLM_MODEL_NAME: str = "deepseek-chat"
    LLM_API_KEY: str = ""
    LLM_API_BASE: str = "https://api.deepseek.com/v1"
    LLM_MAX_TOKENS: int = 8192
    LLM_TEMPERATURE: float = 0.7
    LLM_TOP_P: float = 0.9

    # -------------------------------------------------------------------------
    # Agent 配置
    # -------------------------------------------------------------------------
    AGENT_TIMEOUT: int = 300
    MAX_AGENT_RETRIES: int = 3
    AGENT_CONCURRENT_LIMIT: int = 5

    # -------------------------------------------------------------------------
    # 工具调用配置
    # -------------------------------------------------------------------------
    TOOL_EXECUTION_TIMEOUT: int = 120
    ENABLE_GIT_TOOL: bool = True
    ENABLE_DOCKER_TOOL: bool = True
    ENABLE_CICD_TOOL: bool = True

    # -------------------------------------------------------------------------
    # 安全配置
    # -------------------------------------------------------------------------
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440

    # -------------------------------------------------------------------------
    # 路径配置
    # -------------------------------------------------------------------------
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    LOG_DIR: Path = PROJECT_ROOT / "logs"
    DATA_DIR: Path = PROJECT_ROOT / "data"
    PROMPT_DIR: Path = PROJECT_ROOT / "prompts"

    # -------------------------------------------------------------------------
    # 模型配置
    # -------------------------------------------------------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


settings = Settings()