from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from WTW_app.postgreSQL.db_utils import Base


class Films(Base):
    """Class that holds general data for films."""

    __tablename__ = "films"

    film_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    rate = Column(Float, nullable=False)
    img_url = Column(String, nullable=True)

    details_id = Column(
        Integer, ForeignKey("details.details_id", ondelete="CASCADE"), nullable=False
    )
    details = relationship("Details", cascade="all, delete")


class Details(Base):
    """Class that holds detailed data for films."""

    __tablename__ = "details"

    details_id = Column(Integer, primary_key=True, index=True)
    director = Column(String, nullable=False)
    description = Column(String, nullable=False)


class Times(Base):
    """Class that holds times of requested database operations."""

    __tablename__ = "times"

    time_id = Column(Integer, primary_key=True, index=True)
    database = Column(String, nullable=False)
    request_type = Column(String, nullable=False)
    time_value = Column(Float, nullable=False)
