import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from WTW_app.settings.app_settings import APP_SETTINGS
from WTW_app.routers.films import films_router
from WTW_app.routers.directors import directors_router

logger = logging.getLogger()


app = FastAPI(title=APP_SETTINGS.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=APP_SETTINGS.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# async def startup_db():
#     from WTW_app.db import Base, engine, get_db_session
#     from WTW_app.models.db_models import FilmDBModel, DirectorDBModel

#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     db_session_cm = get_db_session()

#     with db_session_cm as db_session:
#         directors = [
#             DirectorDBModel(name="Frank Darabont"),
#             DirectorDBModel(name="Francis Ford Coppola"),
#             DirectorDBModel(name="Christopher Nolan"),
#             DirectorDBModel(name="Steven Spielberg"),
#             DirectorDBModel(name="Sidney Lumet"),
#         ]
#         for director in directors:
#             db_session.add(director)

#         db_session.commit()

#     print("Database created")


async def scrap_data():
    import requests
    from bs4 import BeautifulSoup
    from tqdm import tqdm
    from WTW_app.repositories.interfaces import IFilmsRepository
    from WTW_app.repositories.films_in_memory import FILMS_REPOSITORY

    print("Data scrapping started...")
    print("Getting the data responses...")

    responses = []

    for url in APP_SETTINGS.scrap_data_urls:
        partial_list_response = requests.get(url)
        responses.append(partial_list_response)

    print("Extracting the data responses...")

    movies_list = []

    for resp in responses:
        partial_s_list = BeautifulSoup(resp.text, "html.parser")
        movies = partial_s_list.find_all("div", class_="lister-item mode-advanced")
        movies_list.append(movies)

    movies_list = [movie for m_list in movies_list for movie in m_list]

    print("Scrapping movies' data:")

    for movie in tqdm(movies_list):
        # Get the movie's title
        title_element = movie.find("h3").find("a")
        if title_element is not None:
            title = title_element.text
        else:
            title = "Title not found"

        # Get the link providing to the movie's details
        f_details_reflink = movie.find("h3").find("a")["href"]
        film_details_url = f"https://www.imdb.com{f_details_reflink}fullcredits"

        # Get the year of movie's production
        year_element = movie.find("h3").find("span", class_="lister-item-year")
        if year_element is not None:
            year = year_element.text.split(" ")
            if len(year) > 1:
                year = year[1].strip("()")
            else:
                year = year[0].strip("()")
            year = int(year)
        else:
            year = 2000

        # Get the movie's rating
        rate_element = movie.find("div", class_="ratings-bar").find("strong")
        if rate_element is not None:
            rate = rate_element.text
            rate = float(rate)
        else:
            rate = 6.6

        # Get the movie's description
        paragraphs = movie.find_all("p", class_="text-muted")
        description_element = paragraphs[1]
        if description_element is not None:
            description = description_element.text.strip()
        else:
            description = "Description not found"

        # Get the movie's image url
        details_response = requests.get(film_details_url)
        soup_details = BeautifulSoup(details_response.text, "html.parser")
        img_url_element = soup_details.find("div", class_="subpage_title_block").find(
            "img", class_="poster"
        )
        if img_url_element is not None:
            img_url = img_url_element["src"]
        else:
            img_url = None

        films_repository: IFilmsRepository = FILMS_REPOSITORY

        films_repository.add_film(
            title=title, year=year, rate=rate, img_url=img_url, director_id=1
        )


# app.add_event_handler("startup", startup_db)
app.add_event_handler("startup", scrap_data)

app.include_router(films_router)
app.include_router(directors_router)
