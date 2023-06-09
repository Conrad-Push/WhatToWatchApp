import typing as tp

from pydantic import BaseModel


class DataGenerationResponse(BaseModel):
    message: str
    execution_time: tp.Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "message": "Data for 1000 films has been generated",
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
    execution_time: tp.Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "message": "Data for 250 films has been scrapped",
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


class DatabaseInfoResponse(BaseModel):
    message: str
    db_state: tp.Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "message": "Database created",
                "db_state": "Created",
            }
        }


class TableDetailsResponse(BaseModel):
    name: str
    size: str

    class Config:
        schema_extra = {
            "example": {
                "name": "films",
                "size": "420 mB",
            }
        }


class TablesInfoResponse(BaseModel):
    message: str
    tables_details: tp.List[TableDetailsResponse]

    class Config:
        schema_extra = {
            "example": {
                "message": "Database restarted",
                "tables": [
                    {
                        "name": "films",
                        "size": "420 mb",
                    },
                    {
                        "name": "details",
                        "size": "997 mb",
                    },
                ],
            }
        }
