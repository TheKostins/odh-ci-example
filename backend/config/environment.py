from functools import lru_cache
from pydantic.networks import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_url: PostgresDsn = PostgresDsn(url = 'postgresql+psycopg://postgres:postgres@localhost:5432/ci-example')
    port: int = 8080

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
