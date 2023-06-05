from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from WTW_app.db import Base


class Films(Base):
    """Class that holds general data for films."""

    __tablename__ = "films"

    film_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    year = Column(Integer, nullable=False)
    rate = Column(Float, nullable=False)
    img_url = Column(String, nullable=True)

    details_id = Column(Integer, ForeignKey("details.details_id"), nullable=False)
    details = relationship("Details")


class Details(Base):
    """Class that holds detailed data for films."""

    __tablename__ = "details"

    details_id = Column(Integer, primary_key=True, index=True)
    director = Column(String, nullable=False)
    description = Column(String, nullable=False)
