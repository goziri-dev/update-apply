from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(Path(__file__).parent / ".env")


class _Settings(BaseSettings):
    DB_URL: PostgresDsn = Field(alias="DB_URL")
    SERVER_HOST: str = Field(alias="SERVER_HOST", default="127.0.0.1")
    SERVER_PORT: int = 8000
    TECHMAP_API_KEY: str = Field(alias="TECHMAP_API_KEY", default="")

    model_config = SettingsConfigDict(extra="forbid", env_file=".env")

    @field_validator("SERVER_HOST", mode="before")
    @classmethod
    def set_default_server(cls, v: str) -> str:
        return v or "127.0.0.1"


settings = _Settings()  # type: ignore[call-arg]