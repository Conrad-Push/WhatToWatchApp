import typing as tp

from abc import ABC, abstractmethod
from WTW_app.directors.schema import DirectorResponse


class IDirectorsRepository(ABC):
    @abstractmethod
    def get_directors(self) -> tp.List[DirectorResponse]:
        pass

    @abstractmethod
    def add_director(self, *, name: str) -> DirectorResponse:
        pass

    @abstractmethod
    def modify_director(self, *, director_id: int, name: str) -> DirectorResponse:
        pass

    @abstractmethod
    def remove_director(self, *, director_id: int) -> DirectorResponse:
        pass
