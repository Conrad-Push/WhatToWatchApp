import logging
import time
import typing as tp

from WTW_app.models import Details
from WTW_app.details.schema import DetailsResponse, DetailsListResponse
from WTW_app.details.interface import IDetailsRepository
from WTW_app.postgreSQL_db import set_db_connection

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

logger = logging.getLogger()


class DetailsRepository(IDetailsRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_details_list(self) -> DetailsListResponse:
        _details_list: tp.List[DetailsResponse] = []

        start_time = time.time()

        query_details = self.session.query(Details)

        _details_db: tp.List[Details] = query_details.all()

        end_time = time.time()
        execution_time = end_time - start_time

        _details = [DetailsResponse.from_orm(x) for x in _details_db]

        _details_list: DetailsListResponse = DetailsListResponse(
            details=_details,
            execution_time=execution_time,
        )

        return _details_list

    def get_details(self, *, details_id: int) -> DetailsResponse:
        _details: DetailsResponse

        start_time = time.time()

        query_details = self.session.query(Details)
        _details_db = query_details.get(details_id)

        end_time = time.time()
        execution_time = end_time - start_time

        if _details_db:
            _details = DetailsResponse.from_orm(_details_db)
            _details.execution_time = execution_time
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
                start_time = time.time()

                self.session.add(_details_db)
                self.session.commit()
                logger.info(
                    f"A film details was added with id: {_details_db.details_id}"
                )

                end_time = time.time()
                execution_time = end_time - start_time

                _details = DetailsResponse.from_orm(_details_db)
                _details.execution_time = execution_time

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
        database = "postgresql"
        request_type = "PATCH"

        _details: DetailsResponse

        start_time = time.time()

        query_details = self.session.query(Details)
        _details_db = query_details.get(details_id)

        if not _details_db:
            _details = None
        else:
            if director is not None and _details_db.director != director:
                _details_db.director = director
            if description is not None and _details_db.description != description:
                _details_db.description = description

        self.session.commit()

        end_time = time.time()
        execution_time = end_time - start_time

        _details = DetailsResponse.from_orm(_details_db)
        _details.execution_time = execution_time

        conn = set_db_connection()
        cur = conn.cursor()

        times_values = (
            database,
            request_type,
            execution_time,
        )

        cur.execute(
            """
        INSERT INTO times (database, request_type, time_value)
        VALUES (%s, %s, %s)
        """,
            times_values,
        )

        conn.commit()

        cur.close()
        conn.close()

        return _details

    def remove_details(self, *, details_id: int) -> DetailsResponse:
        _details: DetailsResponse

        start_time = time.time()

        query_details = self.session.query(Details)
        _details_db = query_details.get(details_id)

        if _details_db:
            _details = DetailsResponse.from_orm(_details_db)

            self.session.delete(_details_db)
            self.session.commit()

            end_time = time.time()
            execution_time = end_time - start_time

            _details.execution_time = execution_time
        else:
            _details = None

        return _details
