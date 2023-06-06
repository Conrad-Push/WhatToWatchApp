import logging
import typing as tp

from WTW_app.models import Details
from WTW_app.details.schema import DetailsResponse
from WTW_app.details.interface import IDetailsRepository

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

logger = logging.getLogger()


class DetailsRepository(IDetailsRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_details_list(self) -> tp.List[DetailsResponse]:
        _details_list: tp.List[DetailsResponse] = []

        query_details = self.session.query(Details)

        _details_db: tp.List[Details] = query_details.all()

        _details_list = [DetailsResponse.from_orm(x) for x in _details_db]

        return _details_list

    def get_details(self, *, details_id: int) -> DetailsResponse:
        _details: DetailsResponse

        query_details = self.session.query(Details)
        _details_db = query_details.get(details_id)

        if _details_db:
            _details = DetailsResponse.from_orm(_details_db)
        else:
            _details = None

        return _details

    def add_details(
        self,
        *,
        director: str,
        description: str,
    ) -> DetailsResponse:
        _details: DetailsResponse

        try:
            _details_db: Details = Details(
                director=director,
                description=description,
            )

            if _details_db:
                self.session.add(_details_db)
                self.session.commit()
                logger.info(
                    f"A film details was added with id: {_details_db.details_id}"
                )
                _details = DetailsResponse.from_orm(_details_db)

        except IntegrityError as e:
            logger.error(f"Failed to add film details to the database. Error: {str(e)}")
            return None

        if not _details_db:
            _details = None

        return _details

    def modify_details(
        self,
        *,
        details_id: int,
        director: tp.Optional[str] = None,
        description: tp.Optional[str] = None,
    ) -> DetailsResponse:
        _details: DetailsResponse

        query_details = self.session.query(Details)
        _details_db = query_details.get(details_id)

        if not _details_db:
            _details = None
        else:
            if director and _details_db.director != director:
                _details_db.director = director
            if description and _details_db.description != description:
                _details_db.description = description

        self.session.commit()
        _details = DetailsResponse.from_orm(_details_db)

        return _details

    def remove_details(self, *, details_id: int) -> DetailsResponse:
        _details: DetailsResponse

        query_details = self.session.query(Details)
        _details_db = query_details.get(details_id)

        if _details_db:
            _details = DetailsResponse.from_orm(_details_db)

            self.session.delete(_details_db)
            self.session.commit()
        else:
            _details = None

        return _details
