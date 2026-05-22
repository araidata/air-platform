from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = (
        "postgresql+psycopg://air_platform:air_platform@localhost:5432/air_platform"
    )
    api_title: str = "County AI Assurance Operations Center API"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
