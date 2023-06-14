import logging

from WTW_app.cassandra.settings.db_settings import DB_SETTINGS

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement
from cassandra.policies import RetryPolicy


logger = logging.getLogger()


def set_db_connection():
    cluster = Cluster(
        contact_points=[DB_SETTINGS.db_host],
        port=DB_SETTINGS.db_port,
    )

    session = cluster.connect()

    return session


def create_keyspace(session):
    session.execute(
        f"CREATE KEYSPACE IF NOT EXISTS {DB_SETTINGS.db_name} WITH replication = {{'class':'SimpleStrategy', 'replication_factor':'1'}}"
    )
    logger.info("Keyspace for Cassandra database created")


def create_tables(session):
    session.execute(
        f"CREATE TYPE IF NOT EXISTS {DB_SETTINGS.db_name}.udt_details ("
        "director text,"
        "description text"
        ")"
    )
    logger.info(f"Details data type has been created in Cassandra database")

    session.execute(
        f"CREATE TABLE IF NOT EXISTS {DB_SETTINGS.db_name}.{DB_SETTINGS.db_table_names[0]} ("
        "film_id UUID PRIMARY KEY,"
        "title text,"
        "year int,"
        "rate float,"
        "img_url text,"
        "details FROZEN<udt_details>"
        ")",
    )

    logger.info(
        f"Table '{DB_SETTINGS.db_table_names[0]}' created in Cassandra database"
    )

    session.execute(
        f"CREATE TABLE IF NOT EXISTS {DB_SETTINGS.db_name}.{DB_SETTINGS.db_table_names[1]} ("
        "time_id UUID PRIMARY KEY,"
        "database text,"
        "request_type text,"
        "time_value float,"
        ")"
    )

    logger.info(
        f"Table '{DB_SETTINGS.db_table_names[1]}' created in Cassandra database"
    )


def init_cassandra_db():
    session = set_db_connection()

    rows = session.execute("SELECT keyspace_name FROM system_schema.keyspaces")

    check = False

    for row in rows:
        if row.keyspace_name == DB_SETTINGS.db_name:
            check = True

    if not check:
        create_keyspace(session)
        create_tables(session)

    session.shutdown()

    logger.info("Cassandra database started")


def check_db_status():
    try:
        session = set_db_connection()

        session.execute(
            f"SELECT now() FROM {DB_SETTINGS.db_name}.{DB_SETTINGS.db_table_names[0]}"
        )
        session.execute(
            f"SELECT now() FROM {DB_SETTINGS.db_name}.{DB_SETTINGS.db_table_names[1]}"
        )
        db_state = "Started"

        session.shutdown()
    except Exception as e:
        logger.error(f"Error connecting to Cassandra: {str(e)}")
        db_state = "Error"

    return db_state


# def get_tables_size():
#     session = set_db_connection()

#     # Replace 'table_name' with your actual table name
#     query = f"SELECT COUNT(*) FROM {DB_SETTINGS.table_name}"
#     result = session.execute(query)
#     count = result.one()[0]

#     session.shutdown()

#     table_details = [{"name": DB_SETTINGS.table_name, "size": count}]

#     return table_details


# def restart_collections():
#     session = set_db_connection()

#     # Replace 'table_name' with your actual table name
#     query = f"TRUNCATE {DB_SETTINGS.table_name}"
#     session.execute(query)

#     session.shutdown()

#     logger.info("Cassandra database tables restarted")
