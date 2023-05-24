import logging
import typing as tp

from WTW_app.models import FilmModel, FilmPrevModel
from pydantic import HttpUrl
from WTW_app.repositories.interfaces import IFilmsRepository
from WTW_app.repositories.directors_in_memory import directors_in_memory

logger = logging.getLogger()


class FilmsInMemory(IFilmsRepository):
    def __init__(self):
        self.storage: tp.Dict[int, FilmModel] = {}
        self.films_sequence = 0

    def get_films(self) -> tp.List[FilmPrevModel]:
        _films: tp.List[FilmModel] = list(self.storage.values())

        if _films:
            logger.info("Retreived films.")
            _prevs: tp.List[FilmPrevModel] = []
            for film in _films:
                _prev: tp.Optional[FilmPrevModel] = FilmPrevModel(
                    film_id=film.film_id,
                    title=film.title,
                    year=film.year,
                    rate=film.rate,
                    img_url=film.img_url,
                )
                _prevs.append(_prev)
        else:
            logger.info("No films found.")

        return _prevs

    def get_film_details(self, *, film_id: int) -> tp.Optional[FilmModel]:
        _film: tp.Optional[FilmModel] = self.storage.get(film_id, None)

        if _film:
            logger.info(
                f"A film's details for the film id: '{film_id}' have been found."
            )
            return _film
        else:
            logger.info(
                f"No film's details for the film id: '{film_id}' have been found."
            )
            return None

    def add_film(
        self,
        *,
        title: str,
        year: str,
        rate: float,
        img_url: tp.Optional[HttpUrl] = None,
        director_id: int,
    ) -> tp.Optional[FilmModel]:
        _film_exists: tp.List[FilmModel] = [
            _film
            for _film in self.storage.values()
            if _film.title == title and _film.year == year and _film.rate == rate
        ]

        if _film_exists:
            logger.warning(
                f"Film with title: '{title}', release year: '{year}' and rate: '{rate}' already exists!"
            )
            return None

        _film_id: int = self.films_sequence + 1
        _film: FilmModel = FilmModel(
            film_id=_film_id,
            title=title,
            year=year,
            rate=rate,
            img_url=img_url,
            director_id=director_id,
            director=directors_in_memory.storage[director_id],
        )
        self.storage[_film_id] = _film

        logger.info(f"A film '{title}' was added with id: {_film_id}")
        self.films_sequence += 1

        return _film

    def modify_film(
        self,
        *,
        film_id: int,
        title: tp.Optional[str] = None,
        year: tp.Optional[int] = None,
        rate: tp.Optional[float] = None,
        img_url: tp.Optional[HttpUrl] = None,
        director_id: tp.Optional[int] = None,
    ) -> tp.Optional[FilmModel]:
        _film: tp.Optional[FilmModel] = self.storage.get(film_id, None)

        if not _film:
            logger.warning(f"Film with id: '{film_id}' does not exist!")
            return None

        if title:
            logger.info(
                f"Changing film's title from '{_film.title}' to '{title}' for film id: '{film_id}'"
            )
            _film.title = title

        if year:
            logger.info(
                f"Changing film's year from '{_film.year}' to '{year}' for film id: '{film_id}'"
            )
            _film.year = year

        if rate:
            logger.info(
                f"Changing film's rate from '{_film.rate}' to '{rate}' for film id: '{film_id}'"
            )
            _film.rate = rate

        if img_url:
            logger.info(
                f"Changing film's preview image URL from '{_film.img_url}' to '{img_url}' for film id: '{film_id}'"
            )
            _film.img_url = img_url

        if director_id:
            logger.info(
                f"Changing film's director id from '{_film.director_id}' to '{director_id}' for film id: '{film_id}'"
            )
            _film.director_id = director_id
            _film.director = directors_in_memory.storage[director_id]

        return _film

    def remove_film(self, *, film_id: int) -> tp.Optional[FilmModel]:
        _film: tp.Optional[FilmModel] = self.storage.get(film_id, None)

        if not _film:
            logger.warning(f"Film with id: '{film_id}' does not exist!")
            return None

        self.storage.pop(film_id)

        logger.info(f"Removed film with id: '{film_id}'")

        return _film


films_in_memory = FilmsInMemory()
