from pydantic import BaseModel, HttpUrl
import typing as tp


class FilmModel(BaseModel):
    film_id: int
    title: str
    year: int
    rate: float
    img_url: HttpUrl
    
    class Config:
        schema_extra = {
            "example": {
                "film_id": 1,
                "title": "Skazani na Shawshank",
                "year": 1994,
                "rate": 9.2,
                "img_url": "https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_UX45_CR0,0,45,67_AL_.jpg"
                }
            }
        
class AddFilmModel(BaseModel):
    title: str
    year: int
    rate: float 
    img_url: HttpUrl
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Siedem",
                "year": 1995,
                "rate": 8.6,
                "img_url": "https://m.media-amazon.com/images/M/MV5BOTUwODM5MTctZjczMi00OTk4LTg3NWUtNmVhMTAzNTNjYjcyXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_UX45_CR0,0,45,67_AL_.jpg"
                }
            }