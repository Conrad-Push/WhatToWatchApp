import typing as tp

from fastapi import APIRouter, Depends
from WTW_app.cassandra.times.schema import (
    TimesListResponse,
    AvailableFilterParamsTimes,
)
from WTW_app.cassandra.times.interface import ITimesRepository
from WTW_app.cassandra.dependencies import get_times_repository

cassandra_times_router = APIRouter(
    prefix="/cassandra/times",
    tags=["Times - Cassandra"],
)


@cassandra_times_router.get(
    "/",
    response_model=TimesListResponse,
)
def get_times_list(
    times_repository: ITimesRepository = Depends(get_times_repository),
    filter_by: tp.Optional[AvailableFilterParamsTimes] = None,
    filter_value: tp.Optional[str] = None,
) -> TimesListResponse:
    _times_list: TimesListResponse = times_repository.get_times(
        filter_by=filter_by,
        filter_value=filter_value,
    )

    return _times_list
