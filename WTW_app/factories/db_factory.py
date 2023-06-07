import logging

from WTW_app.db import Base, engine, check_db_exsits, get_table_sizes

logger = logging.getLogger()


def init_db() -> None:
    if check_db_exsits():
        logger.info("Database created")
    else:
        logger.error("Database not created")


def restart_db() -> None:
    Base.metadata.drop_all(bind=engine)
    logger.info("All tables in database dropped")


def create_db_tables() -> None:
    Base.metadata.create_all(bind=engine)
    logger.info("All tables in database created")


def get_db_size() -> None:
    print(get_table_sizes())
