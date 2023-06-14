from fastapi import Depends

from WTW_app.mongoDB.films.interface import IFilmsRepository
from WTW_app.mongoDB.films.films_repository import FilmsRepository
from WTW_app.mongoDB.times.interface import ITimesRepository
from WTW_app.mongoDB.times.times_repository import TimesRepository
from WTW_app.mongoDB.database.interface import IDatabaseRepository
from WTW_app.mongoDB.database.database_repository import DatabaseRepository


def get_films_repository():
    repository: IFilmsRepository = FilmsRepository()
    yield repository


def get_times_repository():
    repository: ITimesRepository = TimesRepository()
    yield repository


def get_database_repository():
    repository: IDatabaseRepository = DatabaseRepository()
    yield repository
