import typing as tp

from abc import ABC, abstractmethod
from WTW_app.mongoDB.films.schema import (
    FilmResponse,
    FilmsListResponse,
    AvailableSortParamsFilms,
    AvailableFilterParamsFilms,
)

from pydantic import HttpUrl


class IFilmsRepository(ABC):
    @abstractmethod
    def get_films(
        self,
        sort_by: tp.Optional[AvailableSortParamsFilms] = None,
        filter_by: tp.Optional[AvailableFilterParamsFilms] = None,
        filter_value: tp.Optional[str] = None,
    ) -> FilmsListResponse:
        pass

    @abstractmethod
    def get_film_details(self, *, film_id: int) -> FilmResponse:
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def remove_film(self, *, film_id: int) -> FilmResponse:
        pass
