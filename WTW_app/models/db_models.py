from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from WTW_app.db import Base


class FilmDBModel(Base):
    __tablename__ = "films"

    film_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    year = Column(Integer, nullable=False)
    rate = Column(Float, nullable=False)
    img_url = Column(String, nullable=True)

    director_id = Column(Integer, ForeignKey("directors.director_id"), nullable=False)
    director = relationship("DirectorDBModel")


class DirectorDBModel(Base):
    __tablename__ = "directors"

    director_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
