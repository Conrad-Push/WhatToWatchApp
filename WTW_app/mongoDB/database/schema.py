import typing as tp

from pydantic import BaseModel


class CollectionDetailsResponse(BaseModel):
    name: str
    size: str

    class Config:
        schema_extra = {
            "example": {
                "name": "films",
                "size": "420 mB",
            }
        }


class DatabaseInfoResponse(BaseModel):
    message: str
    db_state: tp.Optional[str] = None
    tables_details: tp.List[CollectionDetailsResponse] = None
    execution_time: tp.Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "message": "Databse exists and 2 table(s) have been founded",
                "db_state": "Started",
                "tables_details": [
                    {
                        "name": "films",
                        "size": "420 mb",
                    },
                    {
                        "name": "details",
                        "size": "666 mb",
                    },
                ],
                "execution_time": 2.345,
            }
        }


class DataGenerationResponse(BaseModel):
    message: str
    tables_details: tp.List[CollectionDetailsResponse] = None
    execution_time: tp.Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "message": "Data for 1000 films has been generated",
                "tables_details": [
                    {
                        "name": "films",
                        "size": "420 mb",
                    },
                    {
                        "name": "details",
                        "size": "666 mb",
                    },
                ],
                "execution_time": 2.345,
            }
        }


class DataGenerationRequest(BaseModel):
    data_amount: int

    class Config:
        schema_extra = {
            "example": {
                "data_amount": 1000,
            }
        }


class DataScrappingResponse(BaseModel):
    message: str
    tables_details: tp.List[CollectionDetailsResponse] = None
    execution_time: tp.Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "message": "Data for 250 films has been scrapped",
                "tables_details": [
                    {
                        "name": "films",
                        "size": "420 mb",
                    },
                    {
                        "name": "details",
                        "size": "666 mb",
                    },
                ],
                "execution_time": 2.345,
            }
        }


class DataScrappingRequest(BaseModel):
    data_amount: int

    class Config:
        schema_extra = {
            "example": {
                "data_amount": 250,
            }
        }
