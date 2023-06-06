import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from WTW_app.settings.app_settings import APP_SETTINGS
from WTW_app.factories.db_factory import init_db, get_db_size
from WTW_app.factories.data_factory import scrap_data
from WTW_app.films.router import films_router
from WTW_app.details.router import details_router

FORMAT = "[%(asctime)s][%(levelname)s][%(name)s] %(message)s"
logging.basicConfig(
    format=FORMAT, level=str.upper(APP_SETTINGS.log_level), datefmt="%Y-%m-%d %H:%M:%S"
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


async def startup_db():
    init_db()


async def fill_db():
    scrap_data()


app.add_event_handler("startup", startup_db)
app.add_event_handler("startup", scrap_data)
app.add_event_handler("startup", get_db_size)

app.include_router(films_router)
app.include_router(details_router)
