from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_username: str = Field("user", env="POSTGRES_USERNAME")
    db_password: str = Field("Password", env="POSTGRES_PASSWORD")
    db_host: str = Field("postgres", env="POSTGRES_HOST")
    db_port: str = Field(5432, env="POSTGRES_PORT")
    db_name: str = Field("postgres", env="POSTGRES_NAME")


DB_SETTINGS = Settings()
