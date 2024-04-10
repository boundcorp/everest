from pydantic_settings import BaseSettings


class AuthConfig(BaseSettings):
    API_SECRET_KEY: str
    API_KEY_ALGORITHM: str = "HS256"
    SESSION_COOKIE_NAME: str = "evsession"
