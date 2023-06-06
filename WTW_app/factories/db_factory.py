import logging

from WTW_app.db import Base, engine
from WTW_app.db import get_table_sizes

logger = logging.getLogger()


def init_db() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    logger.info("Database created")


def get_db_size() -> None:
    print(get_table_sizes())
