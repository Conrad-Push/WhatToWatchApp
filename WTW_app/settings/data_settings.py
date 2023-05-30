from pydantic import BaseSettings


class Settings(BaseSettings):
    scrap_data_urls = [
        "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating",
        # "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating&start=51",
        # "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating&start=101",
        # "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating&start=151",
        # "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating&start=201",
    ]


DATA_SETTINGS = Settings()
