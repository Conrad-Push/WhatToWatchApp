import typing as tp

from abc import ABC, abstractmethod
from WTW_app.films.schema import FilmModel, FilmPrevModel
from pydantic import HttpUrl


class IFilmsRepository(ABC):
    @abstractmethod
    def get_films(self) -> tp.List[FilmPrevModel]:
        pass

    @abstractmethod
    def get_film_details(self, *, film_id: int) -> FilmModel:
        pass

    @abstractmethod
    def add_film(
        self,
        *,
        title: str,
        year: str,
        rate: float,
        img_url: tp.Optional[HttpUrl] = None,
        director_id: int
    ) -> FilmModel:
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
        director_id: tp.Optional[int] = None
    ) -> FilmModel:
        pass

    @abstractmethod
    def remove_film(self, *, film_id: int) -> FilmModel:
        pass
