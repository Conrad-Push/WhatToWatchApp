import typing as tp

from abc import ABC, abstractmethod
from WTW_app.details.schema import DetailsResponse


class IDetailsRepository(ABC):
    @abstractmethod
    def get_details_list(self) -> tp.List[DetailsResponse]:
        pass

    @abstractmethod
    def get_details(
        self,
        *,
        details_id: int,
    ) -> DetailsResponse:
        pass

    @abstractmethod
    def add_details(
        self,
        *,
        director: str,
        description: str,
    ) -> DetailsResponse:
        pass

    @abstractmethod
    def modify_details(
        self,
        *,
        details_id: int,
        director: tp.Optional[str] = None,
        description: tp.Optional[str] = None,
    ) -> DetailsResponse:
        pass

    @abstractmethod
    def remove_details(
        self,
        *,
        details_id: int,
    ) -> DetailsResponse:
        pass
