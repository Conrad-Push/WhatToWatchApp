import logging

from fastapi import FastAPI, HTTPException, status
from WTW_app.models import FilmModel, AddFilmModel
from WTW_app.repositories.films_in_memory import films_in_memory
from WTW_app.routers.films import films_router
from WTW_app.settings import SETTINGS

logger = logging.getLogger()

app = FastAPI(title=SETTINGS.app_name)


app.include_router(films_router)