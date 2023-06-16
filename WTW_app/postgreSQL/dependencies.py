from fastapi import Depends
from sqlalchemy.orm import Session

from WTW_app.postgreSQL.db_utils import SessionLocal
from WTW_app.postgreSQL.films.interface import IFilmsRepository
from WTW_app.postgreSQL.films.films_repository import FilmsRepository
from WTW_app.postgreSQL.details.interface import IDetailsRepository
from WTW_app.postgreSQL.details.details_repository import DetailsRepository
from WTW_app.postgreSQL.times.interface import ITimesRepository
from WTW_app.postgreSQL.times.times_repository import TimesRepository
from WTW_app.postgreSQL.database.interface import IDatabaseRepository
from WTW_app.postgreSQL.database.database_repository import DatabaseRepository


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


def get_times_repository(
    session: Session = Depends(get_db),
):
    repository: ITimesRepository = TimesRepository(session)
    yield repository


def get_database_repository():
    repository: IDatabaseRepository = DatabaseRepository()
    yield repository
