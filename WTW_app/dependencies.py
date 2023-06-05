from fastapi import Depends
from sqlalchemy.orm import Session

from WTW_app.db import SessionLocal
from WTW_app.films.interface import IFilmsRepository
from WTW_app.films.films_repository import FilmsRepository
from WTW_app.details.interface import IDetailsRepository
from WTW_app.details.directors_repository import DetailsRepository


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


def get_details_repository(
    session: Session = Depends(get_db),
):
    repository: IDetailsRepository = DetailsRepository(session)
    yield repository
