from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    app_name: str = "What To Watch App"
    log_level: str = Field("info", env="LOG_LEVEL")

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


APP_SETTINGS = Settings()
