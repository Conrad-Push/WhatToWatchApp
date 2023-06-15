from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_username: str = Field("user", env="CASSANDRA_USERNAME")
    db_password: str = Field("Password", env="CASSANDRA_PASSWORD")
    db_host: str = Field("cassandra", env="CASSANDRA_HOST")
    db_port: str = Field(9042, env="CASSANDRA_PORT")
    db_name: str = Field("cassandra", env="CASSANDRA_NAME")

    db_table_names = ["films", "times", "film_id", "time_id"]


DB_SETTINGS = Settings()
