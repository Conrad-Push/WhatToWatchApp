import typing as tp

from abc import ABC, abstractmethod
from WTW_app.times.schema import (
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
