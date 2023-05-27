import typing as tp

from pydantic import BaseModel, HttpUrl, root_validator
from WTW_app.directors.schema import DirectorResponse


class FilmResponse(BaseModel):
    film_id: int
    title: str
    year: int
    rate: float
    img_url: tp.Optional[HttpUrl] = None
    director: DirectorResponse

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "film_id": 1,
                "title": "Skazani na Shawshank",
                "year": 1994,
                "rate": 9.2,
                "img_url": "https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_UX45_CR0,0,45,67_AL_.jpg",
                "director": {
                    "director_id": 1,
                    "name": "Frank Darabont",
                },
            }
        }


class FilmPrevResponse(BaseModel):
    film_id: int
    title: str
    year: int
    rate: float
    img_url: tp.Optional[HttpUrl] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "film_id": 1,
                "title": "Skazani na Shawshank",
                "year": 1994,
                "rate": 9.2,
                "img_url": "https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_UX45_CR0,0,45,67_AL_.jpg",
            }
        }


class FilmRequest(BaseModel):
    title: str
    year: int
    rate: float
    img_url: tp.Optional[HttpUrl] = None
    director_id: int

    class Config:
        schema_extra = {
            "example": {
                "title": "Siedem",
                "year": 1995,
                "rate": 8.6,
                "img_url": "https://m.media-amazon.com/images/M/MV5BOTUwODM5MTctZjczMi00OTk4LTg3NWUtNmVhMTAzNTNjYjcyXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_UX67_CR0,0,67,98_AL_.jpg",
                "director_id": 1,
            }
        }


class PatchFilmRequest(BaseModel):
    title: tp.Optional[str] = None
    year: tp.Optional[int] = None
    rate: tp.Optional[float] = None
    img_url: tp.Optional[HttpUrl] = None
    director_id: tp.Optional[int] = None

    @root_validator(pre=True)
    def at_least_one_not_empty(cls, values):
        if (
            not values.get("title")
            and not values.get("year")
            and not values.get("rate")
            and not values.get("img_url")
            and not values.get("director_id")
        ):
            raise ValueError("At least one of changed properties should not be empty.")
        return values

    class Config:
        schema_extra = {
            "example": {
                "title": "Osiem",
                "year": 2023,
                "rate": 3.7,
                "img_url": "https://m.media-amazon.com/images/M/MV5BN2EyZjM3NzUtNWUzMi00MTgxLWI0NTctMzY4M2VlOTdjZWRiXkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_UY67_CR0,0,45,67_AL_.jpg",
                "director_id": 1,
            }
        }
