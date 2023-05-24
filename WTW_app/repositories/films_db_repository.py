import logging
import typing as tp

from sqlalchemy.exc import IntegrityError
from pydantic import HttpUrl
from WTW_app.db import get_db_session
from WTW_app.models.db_models import FilmDBModel
from WTW_app.models.models import FilmModel, FilmPrevModel
from WTW_app.repositories.interfaces import IFilmsRepository

logger = logging.getLogger()


class FilmsDBRepository(IFilmsRepository):
    def get_films(self) -> tp.List[FilmPrevModel]:
        _films: tp.List[FilmPrevModel] = []

        db_session_connect = get_db_session()

        with db_session_connect as db_session:
            query = db_session.query(FilmDBModel)

            _films_db: tp.List[FilmDBModel] = query.all()

            _films = [FilmPrevModel.from_orm(x) for x in _films_db]

        return _films

    def get_film_details(self, *, film_id: int) -> tp.Optional[FilmModel]:
        _film: tp.Optional[FilmModel]

        db_session_connect = get_db_session()

        with db_session_connect as db_session:
            _film_db = db_session.query(FilmDBModel).get(film_id)

            if film_id:
                _film = FilmModel.from_orm(_film_db)
            else:
                _film = None

        return _film

    def add_film(
        self,
        *,
        title: str,
        year: str,
        rate: float,
        img_url: tp.Optional[HttpUrl] = None,
        director_id: int,
    ) -> tp.Optional[FilmModel]:
        _film: tp.Optional[FilmModel]

        db_session_connect = get_db_session()

        with db_session_connect as db_session:
            try:
                _film_db: FilmDBModel = FilmDBModel(
                    title=title,
                    year=year,
                    rate=rate,
                    img_url=img_url,
                    director_id=director_id,
                )

                if _film_db:
                    db_session.add(_film_db)
                    db_session.commit()
                    _film = FilmModel.from_orm(_film_db)

            except IntegrityError as e:
                logger.error(str(e))
                return None

            logger.info(f"A film '{title}' was added with id: {_film_db.film_id}")

            if not _film_db:
                _film = None

            return _film

    def modify_film(
        self,
        *,
        film_id: int,
        title: tp.Optional[str] = None,
        year: tp.Optional[int] = None,
        rate: tp.Optional[float] = None,
        img_url: tp.Optional[HttpUrl] = None,
        director_id: tp.Optional[int] = None,
    ) -> tp.Optional[FilmModel]:
        _film: tp.Optional[FilmModel]

        db_session_connect = get_db_session()

        with db_session_connect as db_session:
            _film_db: FilmDBModel = db_session.query(FilmDBModel).get(film_id)

            if not _film_db:
                _film = None
            else:
                if title and _film_db.title != title:
                    _film_db.title = title
                if year and _film_db.year != year:
                    _film_db.year = year
                if rate and _film_db.rate != rate:
                    _film_db.rate = rate
                if img_url and _film_db.img_url != img_url:
                    _film_db.img_url = img_url
                if director_id and _film_db.director_id != director_id:
                    _film_db.director_id = director_id

            db_session.commit()
            _film = FilmModel.from_orm(_film_db)

        return _film

    def remove_film(self, *, film_id: int) -> tp.Optional[FilmModel]:
        _film: tp.Optional[FilmModel]

        db_session_connect = get_db_session()

        with db_session_connect as db_session:
            _film_db: FilmDBModel = db_session.query(FilmDBModel).get(film_id)

            if _film_db:
                _film = FilmModel.from_orm(_film_db)

                db_session.delete(_film_db)
                db_session.commit()
            else:
                _film = None

        return _film


FILMS_REPOSITORY = FilmsDBRepository()
