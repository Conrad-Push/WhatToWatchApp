import typing as tp

from abc import ABC, abstractmethod
from WTW_app.models import FilmModel
from pydantic import HttpUrl


class IFilmsRepository(ABC):
    @abstractmethod
    def get_films(self) -> tp.List[FilmModel]:
        pass
    
    @abstractmethod
    def add_film(
        self, 
        *, 
        title: str, 
        year: str, 
        rate: float,
        img_url: HttpUrl
    ) -> tp.Optional[FilmModel]:
        pass
    
    @abstractmethod
    def remove_film(
        self, 
        *, 
        film_id: int
    ) -> tp.Optional[FilmModel]:
        pass