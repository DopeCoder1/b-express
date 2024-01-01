from typing import Any

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

from src.constants import Environment


class Config(BaseSettings):
    """
    Configuration settings for the application.
    """

    DATABASE_USER: str
    DATABASE_PWD: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str

    ENVIRONMENT: Environment = Environment.PRODUCTION
    SITE_DOMAIN: str = "127.0.0.1"

    CORS_ORIGINS: list[str] = []
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str] = ["*"]

    APP_VERSION: str = "1"

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ".env"
    

settings = Config()
DATABASE_URL= f"postgresql+asyncpg://{settings.DATABASE_USER}:{settings.DATABASE_PWD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

app_configs: dict[str, Any] = {"title": "B-EXPRESS API", "description": "API для B-EXPRESS"}
if settings.ENVIRONMENT.is_deployed:
    app_configs["root_path"] = f"/v{settings.APP_VERSION}"
if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None

