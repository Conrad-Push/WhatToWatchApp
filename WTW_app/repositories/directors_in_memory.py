import logging
import typing as tp

from WTW_app.models import DirectorModel
from WTW_app.repositories.interfaces import IDirectorsRepository

logger = logging.getLogger()


class DirectorsInMemory(IDirectorsRepository):
    def __init__(self):
        self.storage: tp.Dict[int, DirectorModel] = {}
        self.directors_sequence = 0

    def get_directors(self) -> tp.List[DirectorModel]:
        _directors: tp.List[DirectorModel] = list(self.storage.values())

        if _directors:
            logger.info("Retreived directors.")
        else:
            logger.info("No directors found.")

        return _directors

    def get_director_details(self, *, director_id: int) -> tp.Optional[DirectorModel]:
        _director: tp.Optional[DirectorModel] = self.storage.get(director_id, None)

        if _director:
            logger.info(
                f"A director's details for the director id: '{director_id}' have been found."
            )
            return _director
        else:
            logger.info(
                f"No director's details for the director id: '{director_id}' have been found."
            )
            return None

    def add_director(self, *, name: str) -> tp.Optional[DirectorModel]:
        _director_exists: tp.List[DirectorModel] = [
            _director for _director in self.storage.values() if _director.name == name
        ]

        if _director_exists:
            logger.warning(f"Director with name: '{name}' already exists!")
            return None

        _director_id: int = self.directors_sequence + 1
        _director: DirectorModel = DirectorModel(director_id=_director_id, name=name)
        self.storage[_director_id] = _director

        logger.info(f"A director '{name}' was added with id: {_director_id}")
        self.directors_sequence += 1

        return _director

    def modify_director(
        self, *, director_id: int, name: str
    ) -> tp.Optional[DirectorModel]:
        _director: tp.Optional[DirectorModel] = self.storage.get(director_id, None)

        if not _director:
            logger.warning(f"Director with id: '{director_id}' does not exist!")
            return None

        if name:
            logger.info(
                f"Changing director's name from '{_director.name}' to '{name}' for director id: '{director_id}'"
            )
            _director.name = name

        return _director

    def remove_director(self, *, director_id: int) -> tp.Optional[DirectorModel]:
        _director: tp.Optional[DirectorModel] = self.storage.get(director_id, None)

        if not _director:
            logger.warning(f"Director with id: '{director_id}' does not exist!")
            return None

        self.storage.pop(director_id)

        logger.info(f"Removed director with id: '{director_id}'")

        return _director


DIRECTORS_REPOSITORY = DirectorsInMemory()
DIRECTORS_REPOSITORY.add_director(name="Frank Darabont")
DIRECTORS_REPOSITORY.add_director(name="Francis Ford Coppola")
DIRECTORS_REPOSITORY.add_director(name="Christopher Nolan")
DIRECTORS_REPOSITORY.add_director(name="Sidney Lumet")
