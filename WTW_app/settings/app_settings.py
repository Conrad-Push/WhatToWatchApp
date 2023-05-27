from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    app_name: str = "What To Watch App"
    log_level: str = Field("info", env="LOG_LEVEL")

    origins = [
        "http://localhost",
        "http://localhost:3000",
    ]


APP_SETTINGS = Settings()
