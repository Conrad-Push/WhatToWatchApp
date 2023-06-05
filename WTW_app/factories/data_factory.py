import logging
import requests

from sqlalchemy.orm import Session
from bs4 import BeautifulSoup

from WTW_app.settings.data_settings import DATA_SETTINGS
from WTW_app.db import SessionLocal
from WTW_app.films.interface import IFilmsRepository
from WTW_app.films.films_repository import FilmsRepository
from WTW_app.details.interface import IDetailsRepository
from WTW_app.details.directors_repository import DetailsRepository

logger = logging.getLogger()


def scrap_data():
    session: Session = SessionLocal()

    if session:
        logger.info("Connected with postgreSQL database")
    else:
        logger.error("Connection with postgreSQL database failed")

    films_repository: IFilmsRepository = FilmsRepository(session)
    details_repository: IDetailsRepository = DetailsRepository(session)

    logger.info("Data scrapping started...")
    logger.info("Getting the data responses...")

    responses = []

    for url in DATA_SETTINGS.scrap_data_urls:
        partial_list_response = requests.get(url)
        responses.append(partial_list_response)

    logger.info("Extracting the data responses...")

    movies_list = []

    for resp in responses:
        partial_s_list = BeautifulSoup(resp.text, "html.parser")
        movies = partial_s_list.find_all("div", class_="lister-item mode-advanced")
        movies_list.append(movies)

    movies_list = [movie for m_list in movies_list for movie in m_list]

    logger.info("Scrapping movies' data:")

    for movie in movies_list:
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

        # Get the movie's director
        dir_paragraphs = movie.find("div", class_="lister-item-content").find_all("p")
        director_element = dir_paragraphs[2].find("a")
        if director_element is not None:
            director = director_element.text
        else:
            director = "Director not found"

        # Get the movie's description
        desc_paragraphs = movie.find_all("p", class_="text-muted")
        description_element = desc_paragraphs[1]
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

        _details = details_repository.add_details(
            director=director,
            description=description,
        )

        films_repository.add_film(
            title=title,
            year=year,
            rate=rate,
            img_url=img_url,
            details_id=_details.details_id,
        )

    logger.info("All data added to database")
