from fastapi import Depends
from sqlalchemy.orm import Session

from WTW_app.db import SessionLocal
from WTW_app.films.interface import IFilmsRepository
from WTW_app.films.films_repository import FilmsRepository
from WTW_app.directors.interface import IDirectorsRepository
from WTW_app.directors.directors_repository import DirectorsRepository


def get_db() -> Session:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_films_repository(
    session: Session = Depends(get_db),
):
    repository: IFilmsRepository = FilmsRepository(session)
    yield repository


def get_directors_repository(
    session: Session = Depends(get_db),
):
    repository: IDirectorsRepository = DirectorsRepository(session)
    yield repository
