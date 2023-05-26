from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import create_database, database_exists, drop_database

from WTW_app.settings.db_settings import DB_SETTINGS


DATABASE_URL = (
    f"postgresql://{DB_SETTINGS.db_username}:{DB_SETTINGS.db_password}"
    f"@{DB_SETTINGS.db_host}:{DB_SETTINGS.db_port}/{DB_SETTINGS.db_name}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base(bind=engine)


def check_db_exsits() -> bool:
    return database_exists(engine.url)


def drop_db() -> None:
    return drop_database(engine.url)


def create_db() -> None:
    return create_database(engine.url)
