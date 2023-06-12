import typing as tp

from abc import ABC, abstractmethod
from WTW_app.times.schema import (
    TimesResponse,
    TimesListResponse,
    AvailableFilterParamsTimes,
)


class ITimesRepository(ABC):
    @abstractmethod
    def get_times(
        self,
        filter_by: tp.Optional[AvailableFilterParamsTimes] = None,
        filter_value: tp.Optional[str] = None,
    ) -> TimesListResponse:
        pass

    @abstractmethod
    def add_time(
        self,
        database: str,
        request_type: str,
        time_value: float,
    ) -> TimesResponse:
        pass
