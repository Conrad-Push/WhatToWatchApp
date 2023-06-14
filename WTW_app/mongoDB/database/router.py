from fastapi import APIRouter, Depends

from WTW_app.mongoDB.database.schema import (
    DataGenerationRequest,
    DataGenerationResponse,
    DataScrappingRequest,
    DataScrappingResponse,
    DatabaseInfoResponse,
)
from WTW_app.mongoDB.database.interface import IDatabaseRepository
from WTW_app.mongoDB.dependencies import get_database_repository

mongodb_database_router = APIRouter(
    prefix="/mongodb/database",
    tags=["Database - MongoDB"],
)


@mongodb_database_router.get("/status", response_model=DatabaseInfoResponse)
def check_database_status(
    database_repository: IDatabaseRepository = Depends(get_database_repository),
) -> DatabaseInfoResponse:
    _response = database_repository.check_database_status()

    return _response


@mongodb_database_router.get("/tables/restart", response_model=DatabaseInfoResponse)
def restart_tables_data(
    database_repository: IDatabaseRepository = Depends(get_database_repository),
) -> DatabaseInfoResponse:
    _response = database_repository.restart_tables()

    return _response


@mongodb_database_router.post("/data/generate", response_model=DataGenerationResponse)
def generate_data(
    data_payload: DataGenerationRequest,
    database_repository: IDatabaseRepository = Depends(get_database_repository),
) -> DataGenerationResponse:
    _response = database_repository.generate_data(data_amount=data_payload.data_amount)

    return _response


@mongodb_database_router.post("/data/scrap", response_model=DataScrappingResponse)
def scrap_data(
    data_payload: DataScrappingRequest,
    database_repository: IDatabaseRepository = Depends(get_database_repository),
) -> DataScrappingResponse:
    _response = database_repository.scrap_data(data_amount=data_payload.data_amount)

    return _response
