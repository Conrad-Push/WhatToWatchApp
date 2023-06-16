from WTW_app.cassandra.films.interface import IFilmsRepository
from WTW_app.cassandra.films.films_repository import FilmsRepository
from WTW_app.cassandra.times.interface import ITimesRepository
from WTW_app.cassandra.times.times_repository import TimesRepository
from WTW_app.cassandra.database.interface import IDatabaseRepository
from WTW_app.cassandra.database.database_repository import DatabaseRepository


def get_films_repository():
    repository: IFilmsRepository = FilmsRepository()
    yield repository


def get_times_repository():
    repository: ITimesRepository = TimesRepository()
    yield repository


def get_database_repository():
    repository: IDatabaseRepository = DatabaseRepository()
    yield repository
