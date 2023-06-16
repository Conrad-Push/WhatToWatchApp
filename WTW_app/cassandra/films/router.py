import typing as tp

from fastapi import APIRouter, HTTPException, status, Depends, Query
from WTW_app.cassandra.films.schema import (
    FilmResponse,
    FilmsListResponse,
    FilmRequest,
    PatchFilmRequest,
    AvailableSortParamsFilms,
    AvailableFilterParamsFilms,
)
from WTW_app.cassandra.films.interface import IFilmsRepository
from WTW_app.cassandra.dependencies import get_films_repository

cassandra_films_router = APIRouter(
    prefix="/cassandra/films",
    tags=["Films - Cassandra"],
)


@cassandra_films_router.get(
    "/",
    response_model=FilmsListResponse,
)
def get_films_list(
    films_repository: IFilmsRepository = Depends(get_films_repository),
    page: int = Query(1, ge=1),
    sort_by: tp.Optional[AvailableSortParamsFilms] = None,
    filter_by: tp.Optional[AvailableFilterParamsFilms] = None,
    filter_value: tp.Optional[str] = None,
) -> FilmsListResponse:
    limit = 50
    offset = (page - 1) * limit

    _films_list: FilmsListResponse = films_repository.get_films(
        sort_by=sort_by,
        filter_by=filter_by,
        filter_value=filter_value,
        offset=offset,
        limit=limit,
    )

    return _films_list


@cassandra_films_router.get(
    "/{film_id:int}",
    response_model=FilmResponse,
)
def get_film_details(
    film_id: int,
    films_repository: IFilmsRepository = Depends(get_films_repository),
) -> FilmResponse:
    _film_details: FilmResponse = films_repository.get_film_details(film_id=film_id)

    if not _film_details:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Film's details for given film_id: '{film_id}' have not been found",
        )

    return _film_details


@cassandra_films_router.post(
    "/",
    response_model=FilmResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_film(
    film_payload: FilmRequest,
    films_repository: IFilmsRepository = Depends(get_films_repository),
) -> FilmResponse:
    _film: FilmResponse = films_repository.add_film(
        title=film_payload.title,
        year=film_payload.year,
        rate=film_payload.rate,
        img_url=film_payload.img_url,
        director=film_payload.director,
        description=film_payload.description,
    )

    if not _film:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Error while adding a film - check the inputted data or maybe this film already exists!",
        )

    return _film


@cassandra_films_router.patch(
    "/{film_id:int}",
    response_model=FilmResponse,
)
def modify_film_details(
    film_id: int,
    film_payload: PatchFilmRequest,
    films_repository: IFilmsRepository = Depends(get_films_repository),
) -> FilmResponse:
    _film: FilmResponse = films_repository.modify_film(
        film_id=film_id,
        title=film_payload.title,
        year=film_payload.year,
        rate=film_payload.rate,
        img_url=film_payload.img_url,
        director=film_payload.director,
        description=film_payload.description,
    )

    if not _film:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Cannot modify the film's details!",
        )

    return _film


@cassandra_films_router.delete(
    "/{film_id:int}",
    response_model=FilmResponse,
    responses={404: {"description": "Film for given film_id not found."}},
)
async def delete_film(
    film_id: int,
    films_repository: IFilmsRepository = Depends(get_films_repository),
) -> FilmResponse:
    _film: FilmResponse = films_repository.remove_film(film_id=film_id)

    if not _film:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Film for given film_id: '{film_id}' not found",
        )

    return _film
