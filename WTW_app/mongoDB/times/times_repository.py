import logging
import typing as tp

from WTW_app.mongoDB.models import Times
from WTW_app.mongoDB.times.schema import (
    TimesResponse,
    TimesListResponse,
    AvailableFilterParamsTimes,
)
from WTW_app.mongoDB.times.interface import ITimesRepository


logger = logging.getLogger()


class TimesRepository(ITimesRepository):
    def get_times(
        self,
        filter_by: tp.Optional[AvailableFilterParamsTimes] = None,
        filter_value: tp.Optional[str] = None,
    ) -> TimesListResponse:
        _times: tp.List[TimesResponse] = []

        query = {}

        if filter_by and filter_value:
            filter_field = filter_by.value
            query[filter_field] = filter_value

        _times_db = Times.objects(**query)

        time_values = [time.time_value for time in _times_db]
        times_mean = sum(time_values) / len(time_values) if time_values else None

        for time in _times_db:
            _time: TimesResponse = TimesResponse(
                time_id=time.time_id,
                database=time.database,
                request_type=time.request_type,
                time_value=time.time_value,
            )

            _times.append(_time)

        _times_list: TimesListResponse = TimesListResponse(
            times=_times,
            times_mean=times_mean,
        )

        return _times_list
