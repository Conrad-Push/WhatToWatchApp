import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from WTW_app.settings.app_settings import APP_SETTINGS
from WTW_app.postgreSQL_db import init_db
from WTW_app.films.router import films_router
from WTW_app.details.router import details_router
from WTW_app.times.router import times_router
from WTW_app.database.router import database_router

FORMAT = "[%(asctime)s][%(levelname)s][%(name)s] %(message)s"
logging.basicConfig(
    format=FORMAT,
    level=str.upper(APP_SETTINGS.log_level),
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger()


app = FastAPI(title=APP_SETTINGS.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=APP_SETTINGS.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def start_db():
    init_db()


app.add_event_handler("startup", start_db)


app.include_router(films_router)
app.include_router(details_router)
app.include_router(times_router)
app.include_router(database_router)
