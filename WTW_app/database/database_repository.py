import logging
import random
import time
import requests
import typing as tp

from WTW_app.database.schema import (
    DataGenerationResponse,
    DataScrappingResponse,
    DatabaseInfoResponse,
    TableDetailsResponse,
)
from WTW_app.database.interface import IDatabaseRepository
from WTW_app.postgreSQL_db import Base, engine, set_db_connection, get_table_sizes
from WTW_app.settings.data_settings import DATA_SETTINGS

from sqlalchemy_utils.functions import database_exists
from faker import Faker
from bs4 import BeautifulSoup

logger = logging.getLogger()
logging.getLogger("faker").setLevel(logging.WARNING)


class DatabaseRepository(IDatabaseRepository):
    def check_database_status(self) -> DatabaseInfoResponse:
        start_time = time.time()

        if database_exists(engine.url):
            db_state = "Started"
        else:
            message = "Database is not created"
            db_state = "Error"

        conn = set_db_connection()
        tables = get_table_sizes(conn)
        num_of_tables = len(tables)

        if num_of_tables > 0:
            message = f"Database exists and {num_of_tables} table(s) have been founded"

        tables_details: tp.List[TableDetailsResponse] = []

        for table in tables:
            name, size = table
            table_details: TableDetailsResponse = TableDetailsResponse(
                name=name,
                size=size,
            )
            tables_details.append(table_details)

        end_time = time.time()
        execution_time = end_time - start_time

        response: DatabaseInfoResponse = DatabaseInfoResponse(
            message=message,
            db_state=db_state,
            tables_details=tables_details,
            execution_time=execution_time,
        )

        return response

    def restart_tables(self) -> DatabaseInfoResponse:
        start_time = time.time()

        if database_exists(engine.url):
            Base.metadata.drop_all(bind=engine)
            Base.metadata.create_all(bind=engine)
            message = "Table(s) have been cleared and restarted"
            db_state = "Started"
        else:
            message = "Database error while clearing the tables"
            db_state = "Error"

        tables_details: tp.List[TableDetailsResponse] = []

        conn = set_db_connection()
        tables = get_table_sizes(conn)
        for table in tables:
            name, size = table
            table_details: TableDetailsResponse = TableDetailsResponse(
                name=name,
                size=size,
            )
            tables_details.append(table_details)

        end_time = time.time()
        execution_time = end_time - start_time

        response: DatabaseInfoResponse = DatabaseInfoResponse(
            message=message,
            db_state=db_state,
            tables_details=tables_details,
            execution_time=execution_time,
        )

        return response

    def generate_data(
        self,
        *,
        data_amount: int,
    ) -> DataGenerationResponse:
        faker = Faker()
        data = []

        logger.info(f"Start generating data for {data_amount} film(s)")

        start_time = time.time()

        for _ in range(data_amount):
            film = {
                "title": faker.text(max_nb_chars=50)[:-1],
                "year": faker.random_int(min=1900, max=2023),
                "rate": faker.pyfloat(left_digits=1, right_digits=1, positive=True),
                "img_url": random.choice(DATA_SETTINGS.img_urls),
                "details": {
                    "director": faker.name(),
                    "description": faker.paragraph(),
                },
            }

            data.append(film)

        logger.info(
            f"Establishing connection with database and start inputting data for {data_amount} film(s)"
        )

        conn = set_db_connection()
        cur = conn.cursor()

        for film in data:
            details_values = (
                film["details"]["director"],
                film["details"]["description"],
            )
            cur.execute(
                """
            INSERT INTO details (director, description)
            VALUES (%s, %s)
            RETURNING details_id
            """,
                details_values,
            )
            details_id = cur.fetchone()[0]

            film_values = (
                film["title"],
                film["year"],
                film["rate"],
                film["img_url"],
                details_id,
            )
            cur.execute(
                """
            INSERT INTO films (title, year, rate, img_url, details_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
                film_values,
            )

        conn.commit()

        cur.close()

        tables = get_table_sizes(conn)
        tables_details: tp.List[TableDetailsResponse] = []

        for table in tables:
            name, size = table
            table_details: TableDetailsResponse = TableDetailsResponse(
                name=name,
                size=size,
            )
            tables_details.append(table_details)

        conn.close()

        end_time = time.time()
        execution_time = end_time - start_time

        message = f"Data for {data_amount} film(s) has been generated"

        response = DataGenerationResponse(
            message=message,
            tables_details=tables_details,
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

        data = []

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

            film = {
                "title": title,
                "year": year,
                "rate": rate,
                "img_url": img_url,
                "details": {
                    "director": director,
                    "description": description,
                },
            }

            data.append(film)

        conn = set_db_connection()
        cur = conn.cursor()

        for film in data:
            details_values = (
                film["details"]["director"],
                film["details"]["description"],
            )
            cur.execute(
                """
            INSERT INTO details (director, description)
            VALUES (%s, %s)
            RETURNING details_id
            """,
                details_values,
            )
            details_id = cur.fetchone()[0]

            film_values = (
                film["title"],
                film["year"],
                film["rate"],
                film["img_url"],
                details_id,
            )
            cur.execute(
                """
            INSERT INTO films (title, year, rate, img_url, details_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
                film_values,
            )

        conn.commit()

        cur.close()

        tables = get_table_sizes(conn)
        tables_details: tp.List[TableDetailsResponse] = []

        for table in tables:
            name, size = table
            table_details: TableDetailsResponse = TableDetailsResponse(
                name=name,
                size=size,
            )
            tables_details.append(table_details)

        conn.close()

        end_time = time.time()
        execution_time = end_time - start_time

        message = f"Data for {data_amount} film(s) has been scrapped"

        response = DataScrappingResponse(
            message=message,
            tables_details=tables_details,
            execution_time=execution_time,
        )

        return response
