import logging
import typing as tp

from WTW_app.models import Film
from WTW_app.films.schema import (
    FilmResponse,
    FilmPrevResponse,
    AvailableSortParamsFilms,
    AvailableFilterParamsFilms,
)
from WTW_app.films.interface import IFilmsRepository

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from pydantic import HttpUrl

logger = logging.getLogger()


class FilmsRepository(IFilmsRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_films(
        self,
        sort_by: tp.Optional[AvailableSortParamsFilms] = None,
        filter_by: tp.Optional[AvailableFilterParamsFilms] = None,
        filter_value: tp.Optional[str] = None,
    ) -> tp.List[FilmPrevResponse]:
        _films: tp.List[FilmPrevResponse] = []
        sort_by_val = getattr(Film, sort_by.value) if sort_by else None
        filter_by_val = getattr(Film, filter_by.value) if filter_by else None

        query_films = self.session.query(Film)

        if sort_by_val:
            query_films = query_films.order_by(sort_by_val)

        if filter_by_val and filter_value is not None:
            query_films = query_films.filter(filter_by_val.ilike(f"%{filter_value}%"))

        _films_db: tp.List[Film] = query_films.all()

        _films = [FilmPrevResponse.from_orm(x) for x in _films_db]

        return _films

    def get_film_details(self, *, film_id: int) -> FilmResponse:
        _film: FilmResponse

        query_films = self.session.query(Film)
        _film_db = query_films.get(film_id)

        if _film_db:
            _film = FilmResponse.from_orm(_film_db)
        else:
            _film = None

        return _film

    def add_film(
        self,
        *,
        title: str,
        description: str,
        year: str,
        rate: float,
        img_url: tp.Optional[HttpUrl] = None,
        director_id: int,
    ) -> FilmResponse:
        _film: FilmResponse

        try:
            _film_db: Film = Film(
                title=title,
                description=description,
                year=year,
                rate=rate,
                img_url=img_url,
                director_id=director_id,
            )

            if _film_db:
                self.session.add(_film_db)
                self.session.commit()
                _film = FilmResponse.from_orm(_film_db)

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
        description: tp.Optional[str] = None,
        year: tp.Optional[int] = None,
        rate: tp.Optional[float] = None,
        img_url: tp.Optional[HttpUrl] = None,
        director_id: tp.Optional[int] = None,
    ) -> FilmResponse:
        _film: FilmResponse

        query_films = self.session.query(Film)
        _film_db = query_films.get(film_id)

        if not _film_db:
            _film = None
        else:
            if title and _film_db.title != title:
                _film_db.title = title
            if description and _film_db.description != description:
                _film_db.description = description
            if year and _film_db.year != year:
                _film_db.year = year
            if rate and _film_db.rate != rate:
                _film_db.rate = rate
            if img_url and _film_db.img_url != img_url:
                _film_db.img_url = img_url
            if director_id and _film_db.director_id != director_id:
                _film_db.director_id = director_id

        self.session.commit()
        _film = FilmResponse.from_orm(_film_db)

        return _film

    def remove_film(self, *, film_id: int) -> FilmResponse:
        _film: FilmResponse

        query_films = self.session.query(Film)
        _film_db = query_films.get(film_id)

        if _film_db:
            _film = FilmResponse.from_orm(_film_db)

            self.session.delete(_film_db)
            self.session.commit()
        else:
            _film = None

        return _film
