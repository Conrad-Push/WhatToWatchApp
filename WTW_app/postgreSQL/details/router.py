import typing as tp

from fastapi import APIRouter, HTTPException, status, Depends
from WTW_app.postgreSQL.details.schema import (
    DetailsResponse,
    DetailsListResponse,
    DetailsRequest,
    PatchDetailsRequest,
)
from WTW_app.postgreSQL.details.interface import IDetailsRepository
from WTW_app.postgreSQL.dependencies import get_details_repository

postgres_details_router = APIRouter(
    prefix="/postgresql/details",
    tags=["Details - PostgreSQL"],
)


@postgres_details_router.get(
    "/",
    response_model=DetailsListResponse,
)
def get_details_list(
    details_repository: IDetailsRepository = Depends(get_details_repository),
) -> DetailsListResponse:
    _details_list = details_repository.get_details_list()

    return _details_list


@postgres_details_router.get(
    "/{details_id:int}",
    response_model=DetailsResponse,
)
def get_details(
    details_id: int,
    details_repository: IDetailsRepository = Depends(get_details_repository),
) -> DetailsResponse:
    _details: DetailsResponse = details_repository.get_details(
        details_id=details_id,
    )

    if not _details:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Film's details for given details id: '{details_id}' have not been found",
        )

    return _details


@postgres_details_router.post(
    "/",
    response_model=DetailsResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_details(
    details_payload: DetailsRequest,
    details_repository: IDetailsRepository = Depends(get_details_repository),
) -> DetailsResponse:
    _details: DetailsResponse = details_repository.add_details(
        director=details_payload.director,
        description=details_payload.description,
    )

    if not _details:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Error while adding a details",
        )

    return _details


@postgres_details_router.patch(
    "/{details_id:int}",
    response_model=DetailsResponse,
)
def modify_details(
    details_id: int,
    details_payload: PatchDetailsRequest,
    details_repository: IDetailsRepository = Depends(get_details_repository),
) -> DetailsResponse:
    _details: DetailsResponse = details_repository.modify_details(
        details_id=details_id,
        director=details_payload.director,
        description=details_payload.description,
    )

    if not _details:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Cannot modify the film's details!",
        )

    return _details


@postgres_details_router.delete(
    "/{details_id:int}",
    response_model=DetailsResponse,
    responses={404: {"description": "Details for given details id not found."}},
)
async def delete_details(
    details_id: int,
    details_repository: IDetailsRepository = Depends(get_details_repository),
) -> DetailsResponse:
    _details: DetailsResponse = details_repository.remove_details(details_id=details_id)

    if not _details:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Details for given details id: '{details_id}' not found",
        )

    return _details
