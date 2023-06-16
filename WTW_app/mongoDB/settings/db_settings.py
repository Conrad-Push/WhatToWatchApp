from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_username: str = Field("user", env="MONGO_USERNAME")
    db_password: str = Field("Password", env="MONGO_PASSWORD")
    db_host: str = Field("mongodb", env="MONGO_HOST")
    db_port: str = Field(27017, env="MONGO_PORT")
    db_name: str = Field("mongodb", env="MONGO_NAME")


DB_SETTINGS = Settings()
