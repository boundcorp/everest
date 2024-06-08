import os

from pydantic_settings import BaseSettings


def env_variable_truthy(key, default=""):
    return os.environ.get(key, default).lower().strip() in ["1", "true", "t", "y"]


INGRESS_PORT = int(os.environ.get("INGRESS_PORT", 80))


class AuthConfig(BaseSettings):
    API_SECRET_KEY: str
    API_KEY_ALGORITHM: str = "HS256"
    SESSION_COOKIE_NAME: str = "evsession"


class DevContainerConfig(BaseSettings):
    INGRESS_PORT: int = INGRESS_PORT


class StorageConfig(BaseSettings):
    MINIO_ENDPOINT: str = os.environ.get("MINIO_ENDPOINT", "minio:9000")
    MINIO_ACCESS_KEY: str = os.environ.get("MINIO_ACCESS_KEY", "dev")
    MINIO_SECRET_KEY: str = os.environ.get("MINIO_SECRET_KEY", "test1234")
    MINIO_MEDIA_BUCKET_NAME: str = os.environ.get("MINIO_MEDIA_BUCKET_NAME", "everest-dev")
    MINIO_USE_HTTPS: bool = env_variable_truthy("MINIO_USE_HTTPS")
    MINIO_AUTO_CREATE_MEDIA_BUCKET: bool = env_variable_truthy("MINIO_AUTO_CREATE_MEDIA_BUCKET", "true")
    MINIO_MEDIA_URL: str = os.environ.get(
        "MINIO_MEDIA_URL", f"http://localhost:{INGRESS_PORT}/{MINIO_MEDIA_BUCKET_NAME}"
    )
    MINIO_MEDIA_USE_PRESIGNED: bool = env_variable_truthy("MINIO_MEDIA_USE_PRESIGNED", "true")
