from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_username: str = Field("DB_USERNAME", env="DB_USERNAME")
    db_password: str = Field("Password", env="DB_PASSWORD")
    db_host: str = Field("DB_HOST", env="DB_HOST")
    db_port: str = Field("5000", env="DB_PORT")
    db_name: str = Field("DB_NAME", env="DB_NAME")


DB_SETTINGS = Settings()
