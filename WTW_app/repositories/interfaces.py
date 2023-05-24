import typing as tp

from abc import ABC, abstractmethod
from WTW_app.models.models import FilmModel, FilmPrevModel, DirectorModel
from pydantic import HttpUrl


class IFilmsRepository(ABC):
    @abstractmethod
    def get_films(self) -> tp.List[FilmPrevModel]:
        pass

    @abstractmethod
    def get_film_details(self, *, film_id: int) -> tp.Optional[FilmModel]:
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
    ) -> tp.Optional[FilmModel]:
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
    ) -> tp.Optional[FilmModel]:
        pass

    @abstractmethod
    def remove_film(self, *, film_id: int) -> tp.Optional[FilmModel]:
        pass


class IDirectorsRepository(ABC):
    @abstractmethod
    def get_directors(self) -> tp.List[DirectorModel]:
        pass

    @abstractmethod
    def add_director(self, *, name: str) -> tp.Optional[DirectorModel]:
        pass

    @abstractmethod
    def modify_director(
        self, *, director_id: int, name: str
    ) -> tp.Optional[DirectorModel]:
        pass

    @abstractmethod
    def remove_director(self, *, director_id: int) -> tp.Optional[DirectorModel]:
        pass
