import typing as t

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from WTW_app.settings.db_settings import DB_SETTINGS


SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_SETTINGS.db_username}:{DB_SETTINGS.db_password}@{DB_SETTINGS.db_host}:{DB_SETTINGS.db_port}/{DB_SETTINGS.db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextmanager
def get_db_session() -> t.Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
