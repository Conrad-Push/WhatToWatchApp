import logging

from fastapi import FastAPI
from WTW_app.routers.films import films_router
from WTW_app.routers.directors import directors_router
from WTW_app.settings import SETTINGS

logger = logging.getLogger()

app = FastAPI(title=SETTINGS.app_name)


app.include_router(films_router)
app.include_router(directors_router)