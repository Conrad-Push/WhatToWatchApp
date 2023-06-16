import logging
import time
import typing as tp

from WTW_app.cassandra.models import Films, Times, Film_Id, Time_Id
from WTW_app.cassandra.films.schema import (
    DetailsSchema,
    FilmResponse,
    FilmPrevResponse,
    FilmsListResponse,
    AvailableSortParamsFilms,
    AvailableFilterParamsFilms,
)
from WTW_app.cassandra.films.interface import IFilmsRepository

from sqlalchemy.exc import IntegrityError
from pydantic import HttpUrl
from math import ceil
from cassandra.util import OrderedMap

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
        database = "cassandra"
        request_type = "GET"
        sort = False
        filter = False

        _films: tp.List[FilmPrevResponse] = []

        start_time = time.time()

        _films_db = Films.objects().limit(None)

        if filter_by and filter_value:
            filter = True
            _films_db = [
                film
                for film in _films_db
                if filter_value.lower() in str(getattr(film, filter_by.value)).lower()
            ]

        if sort_by:
            sort = True
            sort_field = sort_by.value
            _films_db = sorted(_films_db, key=lambda film: getattr(film, sort_field))

        total_count = len(_films_db)

        _films_db = _films_db[offset : offset + limit]

        end_time = time.time()
        execution_time = end_time - start_time

        for film in _films_db:
            _film: FilmPrevResponse = FilmPrevResponse(
                film_id=film.film_id,
                title=film.title,
                year=film.year,
                rate=round(film.rate, 2),
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

        _time_id = Time_Id.objects().filter(Time_Id.id_name == "time_id")
        if not _time_id:
            time_id = 1
            id_name = "time_id"
            Time_Id.create(
                time_id=time_id,
                id_name=id_name,
            )
        else:
            _t_id = _time_id[0]
            time_id = _t_id.time_id + 1
            _t_id.time_id = time_id
            _t_id.save()

        Times.create(
            time_id=time_id,
            database=database,
            request_type=request_type,
            time_value=execution_time,
        )

        return _films_list

    def get_film_details(self, *, film_id: int) -> FilmResponse:
        database = "cassandra"
        request_type = "GET_details"

        _film: FilmResponse

        start_time = time.time()

        _film_db = Films.objects(film_id=film_id)

        end_time = time.time()
        execution_time = end_time - start_time

        if _film_db:
            _film_db = _film_db[0]
            _film = FilmResponse(
                film_id=_film_db.film_id,
                title=_film_db.title,
                year=_film_db.year,
                rate=round(_film_db.rate, 2),
                img_url=_film_db.img_url,
                details=DetailsSchema(
                    director=_film_db.details["director"],
                    description=_film_db.details["description"],
                ),
                execution_time=execution_time,
            )
        else:
            _film = None

        _time_id = Time_Id.objects().filter(Time_Id.id_name == "time_id")
        if not _time_id:
            time_id = 1
            id_name = "time_id"
            Time_Id.create(
                time_id=time_id,
                id_name=id_name,
            )
        else:
            _t_id = _time_id[0]
            time_id = _t_id.time_id + 1
            _t_id.time_id = time_id
            _t_id.save()

        Times.create(
            time_id=time_id,
            database=database,
            request_type=request_type,
            time_value=execution_time,
        )

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
        database = "cassandra"
        request_type = "POST"

        _film: FilmResponse

        _film_id = Film_Id.objects().filter(Film_Id.id_name == "film_id")
        if not _film_id:
            film_id = 1
            id_name = "film_id"
            Film_Id.create(
                film_id=film_id,
                id_name=id_name,
            )
        else:
            _f_id = _film_id[0]
            film_id = _f_id.film_id + 1
            _f_id.film_id = film_id
            _f_id.save()

        try:
            start_time = time.time()

            film_details = OrderedMap(
                [("director", director), ("description", description)]
            )

            _film_db = Films.create(
                film_id=film_id,
                title=title,
                year=year,
                rate=rate,
                img_url=str(img_url),
                details=film_details,
            )

            end_time = time.time()
            execution_time = end_time - start_time

            _film = FilmResponse(
                film_id=_film_db.film_id,
                title=_film_db.title,
                year=_film_db.year,
                rate=round(_film_db.rate, 2),
                img_url=_film_db.img_url,
                details=DetailsSchema(
                    director=_film_db.details["director"],
                    description=_film_db.details["description"],
                ),
                execution_time=execution_time,
            )

        except IntegrityError as e:
            logger.error(str(e))
            return None

        logger.info(f"A film '{title}' was added with id: {_film_db.film_id}")

        if not _film_db:
            _film = None

        _time_id = Time_Id.objects().filter(Time_Id.id_name == "time_id")
        if not _time_id:
            time_id = 1
            id_name = "time_id"
            Time_Id.create(
                time_id=time_id,
                id_name=id_name,
            )
        else:
            _t_id = _time_id[0]
            time_id = _t_id.time_id + 1
            _t_id.time_id = time_id
            _t_id.save()

        Times.create(
            time_id=time_id,
            database=database,
            request_type=request_type,
            time_value=execution_time,
        )

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
        database = "cassandra"
        request_type = "PATCH"

        _film: FilmResponse

        start_time = time.time()

        _film_db = Films.objects(film_id=film_id)

        if not _film_db:
            end_time = time.time()
            execution_time = end_time - start_time
            return None
        else:
            _film_db = _film_db[0]
            if title is not None and _film_db.title != title:
                _film_db.title = title
            if year is not None and _film_db.year != year:
                _film_db.year = year
            if rate is not None and _film_db.rate != rate:
                _film_db.rate = rate
            if img_url is not None and _film_db.img_url != str(img_url):
                _film_db.img_url = str(img_url)
            if director is not None and _film_db.details["director"] != director:
                _film_db.details["director"] = director
            if (
                description is not None
                and _film_db.details["description"] != description
            ):
                _film_db.details["description"] = description

        _film_db.save()

        end_time = time.time()
        execution_time = end_time - start_time

        _film = FilmResponse(
            film_id=_film_db.film_id,
            title=_film_db.title,
            year=_film_db.year,
            rate=round(_film_db.rate, 2),
            img_url=_film_db.img_url,
            details=DetailsSchema(
                director=_film_db.details["director"],
                description=_film_db.details["description"],
            ),
            execution_time=execution_time,
        )

        _time_id = Time_Id.objects().filter(Time_Id.id_name == "time_id")
        if not _time_id:
            time_id = 1
            id_name = "time_id"
            Time_Id.create(
                time_id=time_id,
                id_name=id_name,
            )
        else:
            _t_id = _time_id[0]
            time_id = _t_id.time_id + 1
            _t_id.time_id = time_id
            _t_id.save()

        Times.create(
            time_id=time_id,
            database=database,
            request_type=request_type,
            time_value=execution_time,
        )

        return _film

    def remove_film(self, *, film_id: int) -> FilmResponse:
        database = "cassandra"
        request_type = "DELETE"

        _film: FilmResponse

        start_time = time.time()

        _film_db = Films.objects(film_id=film_id)

        if _film_db:
            _film_db = _film_db[0]
            _film = FilmResponse(
                film_id=_film_db.film_id,
                title=_film_db.title,
                year=_film_db.year,
                rate=round(_film_db.rate, 2),
                img_url=_film_db.img_url,
                details=DetailsSchema(
                    director=_film_db.details["director"],
                    description=_film_db.details["description"],
                ),
            )

            _film_db.delete()

            end_time = time.time()
            execution_time = end_time - start_time

            _film.execution_time = execution_time
        else:
            end_time = time.time()
            execution_time = end_time - start_time

            return None

        _time_id = Time_Id.objects().filter(Time_Id.id_name == "time_id")
        if not _time_id:
            time_id = 1
            id_name = "time_id"
            Time_Id.create(
                time_id=time_id,
                id_name=id_name,
            )
        else:
            _t_id = _time_id[0]
            time_id = _t_id.time_id + 1
            _t_id.time_id = time_id
            _t_id.save()

        Times.create(
            time_id=time_id,
            database=database,
            request_type=request_type,
            time_value=execution_time,
        )

        return _film
