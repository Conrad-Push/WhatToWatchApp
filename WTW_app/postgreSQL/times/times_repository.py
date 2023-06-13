import logging
import typing as tp

from WTW_app.postgreSQL.models import Times
from WTW_app.postgreSQL.times.schema import (
    TimesResponse,
    TimesListResponse,
    AvailableFilterParamsTimes,
)
from WTW_app.postgreSQL.times.interface import ITimesRepository

from sqlalchemy import func
from sqlalchemy.orm import Session

logger = logging.getLogger()


class TimesRepository(ITimesRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_times(
        self,
        filter_by: tp.Optional[AvailableFilterParamsTimes] = None,
        filter_value: tp.Optional[str] = None,
    ) -> TimesListResponse:
        _times: tp.List[TimesResponse] = []
        filter_by_val = getattr(Times, filter_by.value) if filter_by else None

        query_times = self.session.query(Times)

        if filter_by_val and filter_value is not None:
            query_times = query_times.filter(filter_by_val == filter_value)

        _times_db: tp.List[Times] = query_times.all()

        _times_mean = query_times.with_entities(func.avg(Times.time_value)).scalar()

        _times = [TimesResponse.from_orm(x) for x in _times_db]

        _times_list = TimesListResponse(
            times=_times,
            times_mean=_times_mean,
        )

        return _times_list
