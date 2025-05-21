import pathlib

import decouple
from pydantic_settings import BaseSettings

ROOT_DIR = pathlib.Path(__file__).parent.parent.parent.parent.resolve()


class BackendBaseSettings(BaseSettings):
    # Web
    WEB_URL: str = decouple.config("WEB_URL", default="http://localhost:3000")
    LOGGING_LEVEL: str = decouple.config("LOGGING_LEVEL", default="DEBUG")
    IS_ALLOWED_CREDENTIALS: bool = decouple.config("IS_ALLOWED_CREDENTIALS", cast=bool)

    # Database
    POSTGRES_USER: str = decouple.config("POSTGRES_USER")
    POSTGRES_PASSWORD: str = decouple.config("POSTGRES_PASSWORD")
    POSTGRES_DB: str = decouple.config("POSTGRES_DB")
    POSTGRES_PORT: int = decouple.config("POSTGRES_PORT", cast=int)
    POSTGRES_HOST: str = decouple.config("POSTGRES_HOST")

    # CORS
    ALLOWED_ORIGINS: list[str] = ["*"]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]

    class Config:
        env_file = f"{ROOT_DIR}/.env"


settings = BackendBaseSettings()
