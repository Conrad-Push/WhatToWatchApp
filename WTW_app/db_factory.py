import logging

from sqlalchemy.orm import Session

from WTW_app.db import Base, SessionLocal, engine
from WTW_app.models import FilmDBModel, DirectorDBModel

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

    films = [
        FilmDBModel(
            title="Story of my life",
            year=2000,
            rate=9.7,
            img_url="https://m.media-amazon.com/images/M/MV5BYmZlZTMzZTAtZGM5OS00MWU0LTg5YmMtZDJkMDBlMjAxNjViXkEyXkFqcGdeQXVyNDY2NDU1MzA@._V1_QL75_UX140_CR0,0,140,207_.jpg",
            director_id=1,
        ),
        FilmDBModel(
            title="Draw my life",
            year=2023,
            rate=6.9,
            img_url="https://m.media-amazon.com/images/M/MV5BNTA4Yzc4ZTItMTgyOC00MDk2LWE2MzgtZWIwNmY3YjU5YjhjXkEyXkFqcGdeQXVyMTE5MTkxMjAx._V1_QL75_UX140_CR0,0,140,207_.jpg",
            director_id=3,
        ),
    ]
    for film in films:
        session.add(film)

    session.commit()
    logger.info("Database created")
