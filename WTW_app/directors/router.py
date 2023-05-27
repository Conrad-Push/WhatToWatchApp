import typing as tp

from fastapi import APIRouter, HTTPException, status, Depends
from WTW_app.directors.schema import (
    DirectorResponse,
    DirectorRequest,
    PatchDirectorRequest,
)
from WTW_app.directors.interface import IDirectorsRepository
from WTW_app.dependencies import get_directors_repository

directors_router = APIRouter(
    prefix="/directors",
    tags=["Directors"],
)


@directors_router.get("/", response_model=tp.List[DirectorResponse])
def get_directors_list(
    directors_repository: IDirectorsRepository = Depends(get_directors_repository),
) -> tp.List[DirectorResponse]:
    _directors = directors_repository.get_directors()
    return _directors


@directors_router.get("/{director_id:int}", response_model=DirectorResponse)
def get_director_details(
    director_id: int,
    directors_repository: IDirectorsRepository = Depends(get_directors_repository),
) -> DirectorResponse:
    _director_details: DirectorResponse = directors_repository.get_director_details(
        director_id=director_id,
    )

    if not _director_details:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Director's details for given director id: '{director_id}' have not been found",
        )

    return _director_details


@directors_router.post(
    "/", response_model=DirectorResponse, status_code=status.HTTP_201_CREATED
)
def add_director(
    director_payload: DirectorRequest,
    directors_repository: IDirectorsRepository = Depends(get_directors_repository),
) -> DirectorResponse:
    _director: DirectorResponse = directors_repository.add_director(
        name=director_payload.name
    )

    if not _director:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Error while adding a director - check the inputted data or maybe this director already exists!",
        )

    return _director


@directors_router.patch("/{director_id:int}", response_model=DirectorResponse)
def modify_director_details(
    director_id: int,
    director_payload: PatchDirectorRequest,
    directors_repository: IDirectorsRepository = Depends(get_directors_repository),
) -> DirectorResponse:
    _director: DirectorResponse = directors_repository.modify_director(
        director_id=director_id,
        name=director_payload.name,
    )

    if not _director:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Cannot modify the director's details!",
        )

    return _director


@directors_router.delete(
    "/{director_id:int}",
    response_model=DirectorResponse,
    responses={404: {"description": "Director for given director id not found."}},
)
async def delete_director(
    director_id: int,
    directors_repository: IDirectorsRepository = Depends(get_directors_repository),
) -> DirectorResponse:
    _director: DirectorResponse = directors_repository.remove_director(
        director_id == director_id
    )

    if not _director:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Director for given director id: '{director_id}' not found",
        )

    return _director
