import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from WTW_app.settings.app_settings import APP_SETTINGS

from WTW_app.postgreSQL.db_utils import init_postgres_db
from WTW_app.postgreSQL.films.router import postgres_films_router
from WTW_app.postgreSQL.details.router import postgres_details_router
from WTW_app.postgreSQL.times.router import postgres_times_router
from WTW_app.postgreSQL.database.router import postgres_database_router

from WTW_app.mongoDB.db_utils import init_mongo_db
from WTW_app.mongoDB.films.router import mongodb_films_router
from WTW_app.mongoDB.times.router import mongodb_times_router
from WTW_app.mongoDB.database.router import mongodb_database_router

from WTW_app.cassandra.db_utils import init_cassandra_db
from WTW_app.cassandra.films.router import cassandra_films_router
from WTW_app.cassandra.times.router import cassandra_times_router
from WTW_app.cassandra.database.router import cassandra_database_router

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
    init_postgres_db()
    init_mongo_db()
    init_cassandra_db()


app.add_event_handler("startup", start_db)


app.include_router(postgres_films_router)
app.include_router(postgres_details_router)
app.include_router(postgres_times_router)
app.include_router(postgres_database_router)

app.include_router(mongodb_films_router)
app.include_router(mongodb_times_router)
app.include_router(mongodb_database_router)

app.include_router(cassandra_films_router)
app.include_router(cassandra_times_router)
app.include_router(cassandra_database_router)
