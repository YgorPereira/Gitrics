from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # app config props
    APP_NAME: str = "Gitrics"
    APP_DESCRIPTION: str = "Git smart analyzer"
    APP_VERSION: str = "1.0.0"


settings = Settings()
