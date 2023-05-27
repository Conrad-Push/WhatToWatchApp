import logging

from sqlalchemy.orm import Session

from WTW_app.db import Base, SessionLocal, engine
from WTW_app.models import DirectorDBModel

logger = logging.getLogger()


def init_db() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session: Session = SessionLocal()

    directors = [
        DirectorDBModel(name="Frank Darabont"),
        DirectorDBModel(name="Francis Ford Coppola"),
        DirectorDBModel(name="Christopher Nolan"),
        DirectorDBModel(name="Steven Spielberg"),
        DirectorDBModel(name="Sidney Lumet"),
    ]
    for director in directors:
        session.add(director)

    session.commit()
    logger.info("Database created")
