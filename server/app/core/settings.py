from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App config props
    APP_NAME: str = "Gitrics"
    APP_DESCRIPTION: str = "Git smart analyzer"
    APP_VERSION: str = "1.0.0"

    # Postgre config props (from .env)
    PSGRE_USER: str = "postgres"
    PSGRE_PASSWORD: str = ""
    PSGRE_HOST: str = "localhost"
    PSGRE_PORT: int = 5432
    PSGRE_DB: str = "gitrics"

    # Gihtub secrets and callback uri (from .env)
    GITHUB_CLIENT_ID: str = ""

    GITHUB_REDIRECT_URI: str = ""

    # JWT secret key (from .env)
    # SECRET: str

    # Debug boolean from develop enviroment
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://"
            f"{self.PSGRE_USER}:"
            f"{self.PSGRE_PASSWORD}@"
            f"{self.PSGRE_HOST}:"
            f"{self.PSGRE_PORT}/"
            f"{self.PSGRE_DB}"
        )


settings = Settings()
