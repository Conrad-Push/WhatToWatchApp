import typing as tp

from fastapi import FastAPI, HTTPException, status
from WTW_app.models import FilmModel, AddFilmModel
from WTW_app.repositories.films_in_memory import films_in_memory


app = FastAPI(title='What To Watch App Dupa')

@app.get("/films/")
def get_films_list() -> tp.List[FilmModel]:
    _films = films_in_memory.get_films()
    return _films

@app.post("/films/", status_code=status.HTTP_201_CREATED)
def add_film(film_payload: AddFilmModel) -> FilmModel:
    _film: tp.Optional[FilmModel] = films_in_memory.add_film(
        title=film_payload.title,
        year=film_payload.year,
        rate=film_payload.rate,
        img_url=film_payload.img_url
    )
    
    if not _film:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Error while adding a film - check the inputted data or maybe this film already exists!",
        )
        
    return _film

@app.delete(
    "/films/{film_id:int}",
    response_model=FilmModel,
    responses={404: {"description": "Film for given film_id not found."}},
)
async def delete_film(film_id: int):
    _film: tp.Optional[FilmModel] = films_in_memory.remove_film(film_id=film_id)
    
    if not _film:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Film for given film_id: '{film_id}' not found",
        )

    return _film