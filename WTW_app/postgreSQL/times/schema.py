import typing as tp

from enum import Enum
from pydantic import BaseModel


class AvailableFilterParamsTimes(Enum):
    request_type = "request_type"


class TimesResponse(BaseModel):
    time_id: int
    database: str
    request_type: str
    time_value: float

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "time_id": 1,
                "database": "postgresql",
                "request_type": "get_sort",
                "time_value": 1.456,
            }
        }


class TimesListResponse(BaseModel):
    times: tp.List[TimesResponse]
    times_mean: tp.Optional[float] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "times": [
                    {
                        "time_id": 1,
                        "database": "postgresql",
                        "request_type": "get_sort",
                        "time_value": 1.456,
                    },
                    {
                        "time_id": 2,
                        "database": "postgresql",
                        "request_type": "get_filter",
                        "time_value": 2.346,
                    },
                    {
                        "time_id": 3,
                        "database": "postgresql",
                        "request_type": "get_combined",
                        "time_value": 4.679,
                    },
                ],
                "times_mean": 3.245,
            }
        }
