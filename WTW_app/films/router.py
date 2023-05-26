import typing as tp

from fastapi import APIRouter, HTTPException, status, Depends
from WTW_app.films.schema import (
    FilmModel,
    FilmPrevModel,
    AddFilmModel,
    PatchFilmModel,
)
from WTW_app.films.interface import IFilmsRepository
from WTW_app.dependencies import get_films_repository

films_router = APIRouter(
    prefix="/films",
    tags=["Films"],
)


@films_router.get("/", response_model=tp.List[FilmPrevModel])
def get_films_list(
    films_repository: IFilmsRepository = Depends(get_films_repository),
) -> tp.List[FilmPrevModel]:
    _films = films_repository.get_films()
    return _films


@films_router.get("/{film_id:int}", response_model=FilmModel)
def get_film_details(
    film_id: int,
    films_repository: IFilmsRepository = Depends(get_films_repository),
) -> FilmModel:
    _film_details: FilmModel = films_repository.get_film_details(film_id=film_id)

    if not _film_details:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Film's details for given film_id: '{film_id}' have not been found",
        )

    return _film_details


@films_router.post("/", response_model=FilmModel, status_code=status.HTTP_201_CREATED)
def add_film(
    film_payload: AddFilmModel,
    films_repository: IFilmsRepository = Depends(get_films_repository),
) -> FilmModel:
    _film: FilmModel = films_repository.add_film(
        title=film_payload.title,
        year=film_payload.year,
        rate=film_payload.rate,
        img_url=film_payload.img_url,
        director_id=film_payload.director_id,
    )

    if not _film:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Error while adding a film - check the inputted data or maybe this film already exists!",
        )

    return _film


@films_router.patch("/{film_id:int}", response_model=FilmModel)
def modify_film_details(
    film_id: int,
    film_payload: PatchFilmModel,
    films_repository: IFilmsRepository = Depends(get_films_repository),
) -> FilmModel:
    _film: FilmModel = films_repository.modify_film(
        film_id=film_id,
        title=film_payload.title,
        year=film_payload.year,
        rate=film_payload.rate,
        img_url=film_payload.img_url,
        director_id=film_payload.director_id,
    )

    if not _film:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Cannot modify the film's details!",
        )

    return _film


@films_router.delete(
    "/{film_id:int}",
    response_model=FilmModel,
    responses={404: {"description": "Film for given film_id not found."}},
)
async def delete_film(
    film_id: int,
    films_repository: IFilmsRepository = Depends(get_films_repository),
) -> FilmModel:
    _film: FilmModel = films_repository.remove_film(film_id=film_id)

    if not _film:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Film for given film_id: '{film_id}' not found",
        )

    return _film