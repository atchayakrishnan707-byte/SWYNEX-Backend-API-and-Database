
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ScopeSentry API"
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "scopesentry_db"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
