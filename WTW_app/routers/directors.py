import typing as tp

from fastapi import APIRouter, HTTPException, status
from WTW_app.models.models import DirectorModel, AddDirectorModel, PatchDirectorModel
from WTW_app.repositories.interfaces import IDirectorsRepository
from WTW_app.repositories.directors_in_memory import DIRECTORS_REPOSITORY

directors_router = APIRouter(
    prefix="/directors",
    tags=["Directors"],
)


@directors_router.get("/", response_model=tp.List[DirectorModel])
def get_directors_list() -> tp.List[DirectorModel]:
    directors_repository: IDirectorsRepository = DIRECTORS_REPOSITORY

    _directors = directors_repository.get_directors()
    return _directors


@directors_router.get("/{director_id:int}", response_model=tp.Optional[DirectorModel])
def get_director_details(director_id: int) -> tp.Optional[DirectorModel]:
    directors_repository: IDirectorsRepository = DIRECTORS_REPOSITORY

    _director_details: tp.Optional[
        DirectorModel
    ] = directors_repository.get_director_details(director_id=director_id)

    if not _director_details:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Director's details for given director id: '{director_id}' have not been found",
        )

    return _director_details


@directors_router.post(
    "/", response_model=DirectorModel, status_code=status.HTTP_201_CREATED
)
def add_director(director_payload: AddDirectorModel) -> tp.Optional[DirectorModel]:
    directors_repository: IDirectorsRepository = DIRECTORS_REPOSITORY

    _director: tp.Optional[DirectorModel] = directors_repository.add_director(
        name=director_payload.name
    )

    if not _director:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Error while adding a director - check the inputted data or maybe this director already exists!",
        )

    return _director


@directors_router.patch("/{director_id:int}", response_model=tp.Optional[DirectorModel])
def modify_director_details(
    director_id: int, director_payload: PatchDirectorModel
) -> tp.Optional[DirectorModel]:
    directors_repository: IDirectorsRepository = DIRECTORS_REPOSITORY

    _director: tp.Optional[DirectorModel] = directors_repository.modify_director(
        director_id=director_id, name=director_payload.name
    )

    if not _director:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Cannot modify the director's details!",
        )

    return _director


@directors_router.delete(
    "/{director_id:int}",
    response_model=DirectorModel,
    responses={404: {"description": "Director for given director id not found."}},
)
async def delete_director(director_id: int) -> tp.Optional[DirectorModel]:
    directors_repository: IDirectorsRepository = DIRECTORS_REPOSITORY

    _director: tp.Optional[DirectorModel] = directors_repository.remove_director(
        director_id == director_id
    )

    if not _director:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Director for given director id: '{director_id}' not found",
        )

    return _director
