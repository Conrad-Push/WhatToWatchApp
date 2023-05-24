from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # log_level: str = Field(..., env="LOG_LEVEL")
    app_name: str = "What To Watch App"

    origins = [
        "http://localhost",
        "http://localhost:3000",
    ]

    scrap_data_urls = [
        "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating",
        "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating&start=51",
        "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating&start=101",
        "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating&start=151",
        "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating&start=201",
    ]

    # db_username: str = Field(..., env="DB_USERNAME")
    # db_password: str = Field(..., env="DB_PASSWORD")
    # db_host: str = Field(..., env="DB_HOST")
    # db_port: str = Field(..., env="DB_PORT")
    # db_name: str = Field(..., env="DB_NAME")


SETTINGS = Settings()
