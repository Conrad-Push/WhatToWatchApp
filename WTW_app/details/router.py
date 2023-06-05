import typing as tp

from fastapi import APIRouter, HTTPException, status, Depends
from WTW_app.details.schema import (
    DetailsResponse,
    DetailsRequest,
    PatchDetailsRequest,
)
from WTW_app.details.interface import IDetailsRepository
from WTW_app.dependencies import get_details_repository

details_router = APIRouter(
    prefix="/details",
    tags=["Details"],
)


@details_router.get("/", response_model=tp.List[DetailsResponse])
def get_details_list(
    details_repository: IDetailsRepository = Depends(get_details_repository),
) -> tp.List[DetailsResponse]:
    _details = details_repository.get_details_list()
    return _details


@details_router.get("/{details_id:int}", response_model=DetailsResponse)
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


@details_router.post(
    "/", response_model=DetailsResponse, status_code=status.HTTP_201_CREATED
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


@details_router.patch("/{details_id:int}", response_model=DetailsResponse)
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


@details_router.delete(
    "/{details_id:int}",
    response_model=DetailsResponse,
    responses={404: {"description": "Details for given details id not found."}},
)
async def delete_details(
    details_id: int,
    details_repository: IDetailsRepository = Depends(get_details_repository),
) -> DetailsResponse:
    _details: DetailsResponse = details_repository.remove_details(
        details_id == details_id
    )

    if not _details:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Details for given details id: '{details_id}' not found",
        )

    return _details
