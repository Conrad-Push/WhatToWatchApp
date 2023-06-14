import psycopg2
import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from WTW_app.postgreSQL.settings.db_settings import DB_SETTINGS

logger = logging.getLogger()


DATABASE_URL = (
    f"postgresql://{DB_SETTINGS.db_username}:{DB_SETTINGS.db_password}"
    f"@{DB_SETTINGS.db_host}:{DB_SETTINGS.db_port}/{DB_SETTINGS.db_name}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base(bind=engine)


def set_db_connection():
    conn = psycopg2.connect(
        host=DB_SETTINGS.db_host,
        port=DB_SETTINGS.db_port,
        database=DB_SETTINGS.db_name,
        user=DB_SETTINGS.db_username,
        password=DB_SETTINGS.db_password,
    )

    return conn


def init_postgres_db():
    conn = set_db_connection()
    tables = get_table_sizes(conn)

    if len(tables) == 0:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        logger.info("PostgreSQL tables created")

    logger.info("PostgreSQL database started")


def get_table_sizes(conn):
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            relname AS table_name,
            pg_size_pretty(pg_total_relation_size(relid)) AS total_size
        FROM
            pg_catalog.pg_statio_user_tables
        ORDER BY
            pg_total_relation_size(relid) DESC;
    """
    )

    table_sizes = cursor.fetchall()

    cursor.close()
    conn.close()

    return table_sizes
