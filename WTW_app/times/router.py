import typing as tp

from fastapi import APIRouter, HTTPException, status, Depends, Query
from WTW_app.times.schema import (
    TimesResponse,
    TimesListResponse,
    TimesRequest,
    AvailableFilterParamsTimes,
)
from WTW_app.times.interface import ITimesRepository
from WTW_app.dependencies import get_times_repository

times_router = APIRouter(
    prefix="/postgresql/times",
    tags=["Times - PostgreSQL"],
)


@times_router.get(
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


@times_router.post(
    "/",
    response_model=TimesResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_time(
    time_payload: TimesRequest,
    times_repository: ITimesRepository = Depends(get_times_repository),
) -> TimesResponse:
    _time: TimesResponse = times_repository.add_time(
        database=time_payload.database,
        request_type=time_payload.request_type,
        time_value=time_payload.time_value,
    )

    if not _time:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Error while adding a time of executed operation",
        )

    return _time
