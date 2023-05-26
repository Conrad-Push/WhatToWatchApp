import typing as tp

from abc import ABC, abstractmethod
from WTW_app.directors.schema import DirectorModel


class IDirectorsRepository(ABC):
    @abstractmethod
    def get_directors(self) -> tp.List[DirectorModel]:
        pass

    @abstractmethod
    def add_director(self, *, name: str) -> DirectorModel:
        pass

    @abstractmethod
    def modify_director(self, *, director_id: int, name: str) -> DirectorModel:
        pass

    @abstractmethod
    def remove_director(self, *, director_id: int) -> DirectorModel:
        pass
