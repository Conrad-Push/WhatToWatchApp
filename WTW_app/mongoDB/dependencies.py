from fastapi import Depends

from WTW_app.mongoDB.films.interface import IFilmsRepository
from WTW_app.mongoDB.films.films_repository import FilmsRepository
from WTW_app.mongoDB.times.interface import ITimesRepository
from WTW_app.mongoDB.times.times_repository import TimesRepository


def get_films_repository():
    repository: IFilmsRepository = FilmsRepository()
    yield repository


def get_times_repository():
    repository: ITimesRepository = TimesRepository()
    yield repository
