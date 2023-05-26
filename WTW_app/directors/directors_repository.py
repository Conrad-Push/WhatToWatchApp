import logging
import typing as tp

from WTW_app.models import DirectorDBModel
from WTW_app.directors.schema import DirectorModel
from WTW_app.directors.interface import IDirectorsRepository

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

logger = logging.getLogger()


class DirectorsRepository(IDirectorsRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_directors(self) -> tp.List[DirectorModel]:
        _directors: tp.List[DirectorModel] = []

        query_directors = self.session.query(DirectorDBModel)

        _directors_db: tp.List[DirectorDBModel] = query_directors.all()

        _directors = [DirectorModel.from_orm(x) for x in _directors_db]

        return _directors

    def get_director_details(self, *, director_id: int) -> DirectorModel:
        _director: DirectorModel

        query_directors = self.session.query(DirectorDBModel)
        _director_db = query_directors.get(director_id)

        if _director_db:
            _director = DirectorModel.from_orm(_director_db)
        else:
            _director = None

        return _director

    def add_director(
        self,
        *,
        name: str,
    ) -> DirectorModel:
        _director: DirectorModel

        try:
            _director_db: DirectorDBModel = DirectorDBModel(
                name=name,
            )

            if _director_db:
                self.session.add(_director_db)
                self.session.commit()
                _director = DirectorModel.from_orm(_director_db)

        except IntegrityError as e:
            logger.error(str(e))
            return None

        logger.info(
            f"A director '{name}' was added with id: {_director_db.director_id}"
        )

        if not _director_db:
            _director = None

        return _director

    def modify_director(
        self,
        *,
        director_id: int,
        name: str,
    ) -> DirectorModel:
        _director: DirectorModel

        query_directors = self.session.query(DirectorDBModel)
        _director_db = query_directors.get(director_id)

        if not _director_db:
            _director = None
        else:
            if name and _director_db.name != name:
                _director_db.name = name

        self.session.commit()
        _director = DirectorModel.from_orm(_director_db)

        return _director

    def remove_director(self, *, director_id: int) -> DirectorModel:
        _director: DirectorModel

        query_directors = self.session.query(DirectorDBModel)
        _director_db = query_directors.get(director_id)

        if _director_db:
            _director = DirectorModel.from_orm(_director_db)

            self.session.delete(_director_db)
            self.session.commit()
        else:
            _director = None

        return _director
