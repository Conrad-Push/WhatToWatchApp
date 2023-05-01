import logging
import typing as tp

from WTW_app.models import FilmModel
from pydantic import HttpUrl


logger = logging.getLogger()

class FilmsInMemory:
    def __init__(self):
        self.storage: tp.Dict[int, FilmModel] = {}
        self.films_sequence = 0
        
    def get_films(self) -> tp.List[FilmModel]:
        _films: tp.List[FilmModel] = list(self.storage.values())

        if _films:
            logger.info("Retreived films.")
        else:
            logger.info("No films found.")

        return _films
    
    def add_film(
        self, 
        *, 
        title: str, 
        year: str, 
        rate: float,
        img_url: HttpUrl
    ) -> tp.Optional[FilmModel]:
        
        _film_exist: tp.List[FilmModel] = [
            _film
            for _film in self.storage.values()
            if _film.title == title and _film.year == year and _film.rate == rate
        ]
        
        if _film_exist:
            logger.warning(
                f"Film with title: '{title}', release year: '{year}' and rate: '{rate}' already exists!"
            )
            return None
        
        _film_id: int = self.films_sequence + 1
        _film: FilmModel = FilmModel(film_id=_film_id, title=title, year=year, rate=rate, img_url=img_url)
        self.storage[_film_id] = _film

        logger.info(f"A film '{title}' was added with id: {_film_id}")
        self.films_sequence += 1

        return _film
    
    def remove_film(self, *, film_id: int) -> tp.Optional[FilmModel]:
        _film: tp.Optional[FilmModel] = self.storage.get(film_id, None)

        if not _film:
            logger.warning(f"Film with id: '{film_id}' does not exist!")
            return None

        self.storage.pop(film_id)

        logger.info(f"Removed film with id: '{film_id}'")

        return _film
    
    
films_in_memory = FilmsInMemory()
films_in_memory.add_film(title='Skazani na Shawshank', year=1994, rate=9.2, img_url="https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_UX45_CR0,0,45,67_AL_.jpg")
films_in_memory.add_film(title='Ojciec chrzestny', year=1972, rate=9.2, img_url="https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_UY67_CR1,0,45,67_AL_.jpg")
films_in_memory.add_film(title='Mroczny rycerz', year=2008, rate=9.0, img_url="https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_UY67_CR0,0,45,67_AL_.jpg")
films_in_memory.add_film(title='Ojciec chrzestny II', year=1974, rate=9.0, img_url="https://m.media-amazon.com/images/M/MV5BMWMwMGQzZTItY2JlNC00OWZiLWIyMDctNDk2ZDQ2YjRjMWQ0XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_UY67_CR1,0,45,67_AL_.jpg")
films_in_memory.add_film(title='Dwunastu gniewnych ludzi', year=1957, rate=9.0, img_url="https://m.media-amazon.com/images/M/MV5BMWU4N2FjNzYtNTVkNC00NzQ0LTg0MjAtYTJlMjFhNGUxZDFmXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_UX45_CR0,0,45,67_AL_.jpg")