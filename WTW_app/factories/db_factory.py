import logging

from sqlalchemy.orm import Session

from WTW_app.db import Base, engine

logger = logging.getLogger()


def init_db() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    logger.info("Database created")
