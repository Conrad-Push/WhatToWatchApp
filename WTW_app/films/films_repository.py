import logging
import time
import typing as tp

from WTW_app.models import Films
from WTW_app.films.schema import (
    FilmResponse,
    FilmPrevResponse,
    FilmsListResponse,
    AvailableSortParamsFilms,
    AvailableFilterParamsFilms,
)
from WTW_app.films.interface import IFilmsRepository

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from pydantic import HttpUrl
from math import ceil

logger = logging.getLogger()


class FilmsRepository(IFilmsRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_films(
        self,
        limit: int = 50,
        sort_by: tp.Optional[AvailableSortParamsFilms] = None,
        filter_by: tp.Optional[AvailableFilterParamsFilms] = None,
        filter_value: tp.Optional[str] = None,
        offset: int = 0,
    ) -> FilmsListResponse:
        _films: tp.List[FilmPrevResponse] = []
        sort_by_val = getattr(Films, sort_by.value) if sort_by else None
        filter_by_val = getattr(Films, filter_by.value) if filter_by else None

        start_time = time.time()

        query_films = self.session.query(Films)

        if sort_by_val:
            query_films = query_films.order_by(sort_by_val)

        if filter_by_val and filter_value is not None:
            query_films = query_films.filter(filter_by_val.ilike(f"%{filter_value}%"))

        total_count = query_films.count()

        query_films = query_films.offset(offset).limit(limit)

        _films_db: tp.List[Films] = query_films.all()

        end_time = time.time()
        execution_time = end_time - start_time

        _films = [FilmPrevResponse.from_orm(x) for x in _films_db]

        total_pages = ceil(total_count / limit)

        _films_list = FilmsListResponse(
            films=_films,
            total_pages=total_pages,
            execution_time=execution_time,
        )

        return _films_list

    def get_film_details(self, *, film_id: int) -> FilmResponse:
        _film: FilmResponse

        start_time = time.time()

        query_films = self.session.query(Films)
        _film_db = query_films.get(film_id)

        end_time = time.time()
        execution_time = end_time - start_time

        if _film_db:
            _film = FilmResponse.from_orm(_film_db)
            _film.execution_time = execution_time
        else:
            _film = None

        return _film

    def add_film(
        self,
        *,
        title: str,
        year: str,
        rate: float,
        img_url: tp.Optional[HttpUrl] = None,
        details_id: int,
    ) -> FilmResponse:
        _film: FilmResponse

        try:
            _film_db: Films = Films(
                title=title,
                year=year,
                rate=rate,
                img_url=img_url,
                details_id=details_id,
            )

            if _film_db:
                start_time = time.time()

                self.session.add(_film_db)
                self.session.commit()

                end_time = time.time()
                execution_time = end_time - start_time

                _film = FilmResponse.from_orm(_film_db)
                _film.execution_time = execution_time

        except IntegrityError as e:
            logger.error(str(e))
            return None

        logger.info(f"A film '{title}' was added with id: {_film_db.film_id}")

        if not _film_db:
            _film = None

        return _film

    def modify_film(
        self,
        *,
        film_id: int,
        title: tp.Optional[str] = None,
        year: tp.Optional[int] = None,
        rate: tp.Optional[float] = None,
        img_url: tp.Optional[HttpUrl] = None,
        details_id: tp.Optional[int] = None,
    ) -> FilmResponse:
        _film: FilmResponse

        start_time = time.time()

        query_films = self.session.query(Films)
        _film_db = query_films.get(film_id)

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
            if details_id is not None and _film_db.details_id != details_id:
                _film_db.details_id = details_id

        self.session.commit()

        end_time = time.time()
        execution_time = end_time - start_time

        _film = FilmResponse.from_orm(_film_db)
        _film.execution_time = execution_time

        return _film

    def remove_film(self, *, film_id: int) -> FilmResponse:
        _film: FilmResponse

        start_time = time.time()

        query_films = self.session.query(Films)
        _film_db = query_films.get(film_id)

        if _film_db:
            _film = FilmResponse.from_orm(_film_db)

            self.session.delete(_film_db)
            self.session.commit()

            end_time = time.time()
            execution_time = end_time - start_time

            _film.execution_time = execution_time
        else:
            _film = None

        return _film
