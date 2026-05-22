from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = (
        "postgresql+psycopg://air_platform:air_platform@localhost:5432/air_platform"
    )
    api_title: str = "County AI Assurance Operations Center API"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    environment: str = "development"
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    scanner_storage_root: str = "data/scanner-runs"

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.allowed_origins.split(",")
            if origin.strip()
        ]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
