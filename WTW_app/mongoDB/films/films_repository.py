import logging
import time
import typing as tp

from WTW_app.mongoDB.models import Film, Details, Times
from WTW_app.mongoDB.films.schema import (
    DetailsSchema,
    FilmResponse,
    FilmPrevResponse,
    FilmsListResponse,
    AvailableSortParamsFilms,
    AvailableFilterParamsFilms,
)
from WTW_app.mongoDB.films.interface import IFilmsRepository

from sqlalchemy.exc import IntegrityError
from pydantic import HttpUrl
from math import ceil

logger = logging.getLogger()


class FilmsRepository(IFilmsRepository):
    def get_films(
        self,
        limit: int = 50,
        sort_by: tp.Optional[AvailableSortParamsFilms] = None,
        filter_by: tp.Optional[AvailableFilterParamsFilms] = None,
        filter_value: tp.Optional[str] = None,
        offset: int = 0,
    ) -> FilmsListResponse:
        database = "mongodb"
        request_type = "GET"
        sort = False
        filter = False

        _films: tp.List[FilmPrevResponse] = []

        start_time = time.time()

        _films_db = Film.objects

        if sort_by:
            sort = True
            sort_field = sort_by.value
            _films_db = _films_db.order_by(f"{sort_field}")

        if filter_by and filter_value:
            filter = True
            _films_db = _films_db.filter(title__icontains=filter_value)

        total_count = _films_db.count()

        _films_db = _films_db.skip(offset).limit(limit)

        end_time = time.time()
        execution_time = end_time - start_time

        for film in _films_db:
            _film: FilmPrevResponse = FilmPrevResponse(
                film_id=film.film_id,
                title=film.title,
                year=film.year,
                rate=film.rate,
                img_url=film.img_url,
            )

            _films.append(_film)

        total_pages = ceil(total_count / limit)

        _films_list = FilmsListResponse(
            films=_films,
            total_pages=total_pages,
            execution_time=execution_time,
        )

        if sort and filter:
            request_type += "_combined"
        elif sort:
            request_type += "_sort"
        elif filter:
            request_type += "_filter"

        Times(
            database=database,
            request_type=request_type,
            time_value=execution_time,
        ).save()

        return _films_list

    def get_film_details(self, *, film_id: int) -> FilmResponse:
        database = "mongodb"
        request_type = "GET_details"

        _film: FilmResponse

        start_time = time.time()

        film = Film.objects(film_id=film_id).first()

        end_time = time.time()
        execution_time = end_time - start_time

        if film:
            _film = FilmResponse(
                film_id=film.film_id,
                title=film.title,
                year=film.year,
                rate=film.rate,
                img_url=film.img_url,
                details=DetailsSchema(
                    director=film.details.director,
                    description=film.details.description,
                ),
                execution_time=execution_time,
            )
        else:
            _film = None

        Times(
            database=database,
            request_type=request_type,
            time_value=execution_time,
        ).save()

        return _film

    def add_film(
        self,
        *,
        title: str,
        year: str,
        rate: float,
        img_url: tp.Optional[HttpUrl] = None,
        director: str,
        description: str,
    ) -> FilmResponse:
        database = "mongodb"
        request_type = "POST"

        _film: FilmResponse

        try:
            details = Details(director=director, description=description)

            _film_db = Film(
                title=title,
                year=year,
                rate=rate,
                img_url=img_url,
                details=details,
            )

            if _film_db:
                start_time = time.time()

                _film_db.save()

                end_time = time.time()
                execution_time = end_time - start_time

                _film = FilmResponse(
                    film_id=_film_db.film_id,
                    title=_film_db.title,
                    year=_film_db.year,
                    rate=_film_db.rate,
                    img_url=_film_db.img_url,
                    details=DetailsSchema(
                        director=_film_db.details.director,
                        description=_film_db.details.description,
                    ),
                    execution_time=execution_time,
                )

        except IntegrityError as e:
            logger.error(str(e))
            return None

        logger.info(f"A film '{title}' was added with id: {_film_db.film_id}")

        if not _film_db:
            _film = None

        Times(
            database=database,
            request_type=request_type,
            time_value=execution_time,
        ).save()

        return _film

    def modify_film(
        self,
        *,
        film_id: int,
        title: tp.Optional[str] = None,
        year: tp.Optional[int] = None,
        rate: tp.Optional[float] = None,
        img_url: tp.Optional[HttpUrl] = None,
        director: tp.Optional[str] = None,
        description: tp.Optional[str] = None,
    ) -> FilmResponse:
        database = "mongodb"
        request_type = "PATCH"

        _film: FilmResponse

        start_time = time.time()

        _film_db = Film.objects(film_id=film_id).first()

        if not _film_db:
            _film = None
        else:
            if title is not None and _film_db.title != title:
                _film_db.title = title
            if year is not None and _film_db.year != year:
                _film_db.year = year
            if rate is not None and _film_db.rate != rate:
                _film_db.rate = rate
            if img_url is not None and _film_db.img_url != img_url:
                _film_db.img_url = img_url
            if director is not None and _film_db.details.director != director:
                _film_db.details.director = director
            if description is not None and _film_db.details.description != description:
                _film_db.details.description = description

        _film_db.save()

        end_time = time.time()
        execution_time = end_time - start_time

        _film = FilmResponse(
            film_id=_film_db.film_id,
            title=_film_db.title,
            year=_film_db.year,
            rate=_film_db.rate,
            img_url=_film_db.img_url,
            details=DetailsSchema(
                director=_film_db.details.director,
                description=_film_db.details.description,
            ),
            execution_time=execution_time,
        )

        Times(
            database=database,
            request_type=request_type,
            time_value=execution_time,
        ).save()

        return _film

    def remove_film(self, *, film_id: int) -> FilmResponse:
        database = "mongodb"
        request_type = "DELETE"

        _film: FilmResponse

        start_time = time.time()

        _film_db = Film.objects(film_id=film_id).first()

        if _film_db:
            _film = FilmResponse(
                film_id=_film_db.film_id,
                title=_film_db.title,
                year=_film_db.year,
                rate=_film_db.rate,
                img_url=_film_db.img_url,
                details=DetailsSchema(
                    director=_film_db.details.director,
                    description=_film_db.details.description,
                ),
            )

            _film_db.delete()

            end_time = time.time()
            execution_time = end_time - start_time

            _film.execution_time = execution_time
        else:
            _film = None

            end_time = time.time()
            execution_time = end_time - start_time

        Times(
            database=database,
            request_type=request_type,
            time_value=execution_time,
        ).save()

        return _film
