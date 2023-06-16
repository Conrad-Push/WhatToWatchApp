import typing as tp

from pydantic import BaseModel, root_validator


class DetailsResponse(BaseModel):
    details_id: int
    director: str
    description: str
    execution_time: tp.Optional[float] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "details_id": 1,
                "director": "Frank Darabont",
                "description": "Example description",
                "execution_time": 2.345,
            }
        }


class DetailsListResponse(BaseModel):
    details: tp.List[DetailsResponse]
    execution_time: tp.Optional[float] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "details": [
                    {
                        "details_id": 1,
                        "director": "Frank Darabont",
                        "description": "Example description",
                        "execution_time": 2.345,
                    },
                    {
                        "details_id": 2,
                        "director": "Elon Musk",
                        "description": "Example description",
                        "execution_time": 1.345,
                    },
                    {
                        "details_id": 3,
                        "director": "George Lucas",
                        "description": "Example description",
                        "execution_time": 3.666,
                    },
                ],
                "execution_time": 2.345,
            }
        }


class DetailsRequest(BaseModel):
    director: str
    description: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "director": "Elon Musk",
                "description": "To the Moon!",
            }
        }


class PatchDetailsRequest(BaseModel):
    director: tp.Optional[str] = None
    description: tp.Optional[str] = None

    @root_validator(pre=True)
    def not_empty(cls, values):
        if not values.get("director") and not values.get("description"):
            raise ValueError("At least one of changed properties should not be empty.")
        return values

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "director": "John Smith",
                "description": "Modified description.",
            }
        }
