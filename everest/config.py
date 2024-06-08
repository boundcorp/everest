from mountaineer import ConfigBase
from mountaineer.database import DatabaseConfig
from pydantic_settings import SettingsConfigDict

from everest.core.auth.config import AuthConfig, StorageConfig, DevContainerConfig


class AppConfig(ConfigBase, DatabaseConfig, AuthConfig, StorageConfig, DevContainerConfig):
    PACKAGE: str | None = "everest"
    SESSION_COOKIE_NAME: str = "evsession"
    SESSION_JWT_TTL: int = 60 * 60 * 24 * 7
    API_SECRET_KEY: str = "secret"

    model_config = SettingsConfigDict(env_file=(".env",))
