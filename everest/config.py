from mountaineer import ConfigBase
from mountaineer.database import DatabaseConfig
from pydantic_settings import SettingsConfigDict

from everest.core.auth.config import AuthConfig


class AppConfig(ConfigBase, DatabaseConfig, AuthConfig):
    PACKAGE: str | None = "everest"
    SESSION_COOKIE_NAME: str = "evsession"
    API_SECRET_KEY: str = "secret"

    model_config = SettingsConfigDict(env_file=(".env",))
