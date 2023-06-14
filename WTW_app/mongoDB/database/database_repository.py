import logging
import random
import time
import requests
import typing as tp

from WTW_app.mongoDB.models import Film, Details
from WTW_app.mongoDB.database.schema import (
    DataGenerationResponse,
    DataScrappingResponse,
    DatabaseInfoResponse,
    CollectionDetailsResponse,
)
from WTW_app.mongoDB.database.interface import IDatabaseRepository
from WTW_app.mongoDB.db_utils import (
    check_db_status,
    get_collections_size,
    restart_collections,
)
from WTW_app.settings.data_settings import DATA_SETTINGS

from faker import Faker
from bs4 import BeautifulSoup

logger = logging.getLogger()
logging.getLogger("faker").setLevel(logging.WARNING)


class DatabaseRepository(IDatabaseRepository):
    def check_database_status(self) -> DatabaseInfoResponse:
        start_time = time.time()

        db_state = check_db_status()
        if db_state == "Started":
            message = "Database exists"
        else:
            message = "Database is not created"

        collections = get_collections_size()
        num_of_collections = len(collections)

        if num_of_collections > 0:
            message = f"Database exists and {num_of_collections} collection(s) have been founded"

        collections_details: tp.List[CollectionDetailsResponse] = []

        for collection in collections:
            name = collection["name"]
            size = collection["size"]
            collection_details: CollectionDetailsResponse = CollectionDetailsResponse(
                name=name,
                size=size,
            )
            collections_details.append(collection_details)

        end_time = time.time()
        execution_time = end_time - start_time

        response: DatabaseInfoResponse = DatabaseInfoResponse(
            message=message,
            db_state=db_state,
            tables_details=collections_details,
            execution_time=execution_time,
        )

        return response

    def restart_tables(self) -> DatabaseInfoResponse:
        start_time = time.time()

        db_state = check_db_status()
        if db_state:
            restart_collections()
            message = "Collection(s) have been cleared and restarted"
            db_state = "Started"
        else:
            message = "Database error while clearing the collections"
            db_state = "Error"

        collections = get_collections_size()
        collections_details: tp.List[CollectionDetailsResponse] = []

        for collection in collections:
            name = collection["name"]
            size = collection["size"]
            collection_details: CollectionDetailsResponse = CollectionDetailsResponse(
                name=name,
                size=size,
            )
            collections_details.append(collection_details)

        end_time = time.time()
        execution_time = end_time - start_time

        response: DatabaseInfoResponse = DatabaseInfoResponse(
            message=message,
            db_state=db_state,
            tables_details=collections_details,
            execution_time=execution_time,
        )

        return response

    def generate_data(
        self,
        *,
        data_amount: int,
    ) -> DataGenerationResponse:
        faker = Faker()

        logger.info(f"Start generating data for {data_amount} film(s)")

        start_time = time.time()

        for _ in range(data_amount):
            details = Details(director=faker.name(), description=faker.paragraph())

            film = Film(
                title=faker.text(max_nb_chars=50)[:-1],
                year=faker.random_int(min=1900, max=2023),
                rate=faker.pyfloat(left_digits=1, right_digits=1, positive=True),
                img_url=random.choice(DATA_SETTINGS.img_urls),
                details=details,
            )

            if film:
                film.save()

        collections = get_collections_size()
        collections_details: tp.List[CollectionDetailsResponse] = []

        for collection in collections:
            name = collection["name"]
            size = collection["size"]
            collection_details: CollectionDetailsResponse = CollectionDetailsResponse(
                name=name,
                size=size,
            )
            collections_details.append(collection_details)

        end_time = time.time()
        execution_time = end_time - start_time

        message = f"Data for {data_amount} film(s) has been generated"

        response = DataGenerationResponse(
            message=message,
            tables_details=collections_details,
            execution_time=execution_time,
        )

        return response

    def scrap_data(
        self,
        *,
        data_amount: int,
    ) -> DataScrappingResponse:
        if data_amount > 250:
            message = f"Data for {data_amount} film(s) cannot be scrapped because the limit is 250"
            response = DataScrappingResponse(message=message)
            return response

        logger.info(f"Start scrapping data for {data_amount} film(s)")
        logger.info("Getting the data responses...")

        responses = []

        start_time = time.time()

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
        limitted_random_movies = random.sample(movies_list, data_amount)

        logger.info("Scrapping movies' data:")

        for movie in limitted_random_movies:
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
            dir_paragraphs = movie.find("div", class_="lister-item-content").find_all(
                "p"
            )
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
            img_url_element = soup_details.find(
                "div", class_="subpage_title_block"
            ).find("img", class_="poster")
            if img_url_element is not None:
                img_url = img_url_element["src"]
            else:
                img_url = None

            details = Details(director=director, description=description)

            film = Film(
                title=title,
                year=year,
                rate=rate,
                img_url=img_url,
                details=details,
            )

            if film:
                film.save()

        collections = get_collections_size()
        collections_details: tp.List[CollectionDetailsResponse] = []

        for collection in collections:
            name = collection["name"]
            size = collection["size"]
            collection_details: CollectionDetailsResponse = CollectionDetailsResponse(
                name=name,
                size=size,
            )
            collections_details.append(collection_details)

        end_time = time.time()
        execution_time = end_time - start_time

        message = f"Data for {data_amount} film(s) has been scrapped"

        response = DataScrappingResponse(
            message=message,
            tables_details=collections_details,
            execution_time=execution_time,
        )

        return response
