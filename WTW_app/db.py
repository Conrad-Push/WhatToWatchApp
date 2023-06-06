import psycopg2


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import create_database, database_exists, drop_database

from WTW_app.settings.db_settings import DB_SETTINGS


DATABASE_URL = (
    f"postgresql://{DB_SETTINGS.db_username}:{DB_SETTINGS.db_password}"
    f"@{DB_SETTINGS.db_host}:{DB_SETTINGS.db_port}/{DB_SETTINGS.db_name}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base(bind=engine)


def check_db_exsits() -> bool:
    return database_exists(engine.url)


def drop_db() -> None:
    return drop_database(engine.url)


def create_db() -> None:
    return create_database(engine.url)


def get_table_sizes():
    conn = psycopg2.connect(
        host=DB_SETTINGS.db_host,
        port=DB_SETTINGS.db_port,
        database=DB_SETTINGS.db_name,
        user=DB_SETTINGS.db_username,
        password=DB_SETTINGS.db_password,
    )
    cursor = conn.cursor()

    # Query the size of each table
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
