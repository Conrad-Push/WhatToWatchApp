import logging

from WTW_app.cassandra.settings.db_settings import DB_SETTINGS

from cassandra.cluster import Cluster


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
        f"CREATE TABLE IF NOT EXISTS {DB_SETTINGS.db_name}.{DB_SETTINGS.db_table_names[0]} ("
        "film_id int,"
        "title text,"
        "year int,"
        "rate float,"
        "img_url text,"
        "details map<text, text>,"
        "PRIMARY KEY (film_id),"
        ")",
    )

    logger.info(
        f"Table '{DB_SETTINGS.db_table_names[0]}' created in Cassandra database"
    )

    session.execute(
        f"CREATE TABLE IF NOT EXISTS {DB_SETTINGS.db_name}.{DB_SETTINGS.db_table_names[1]} ("
        "time_id int PRIMARY KEY,"
        "database text,"
        "request_type text,"
        "time_value float,"
        ")"
    )

    logger.info(
        f"Table '{DB_SETTINGS.db_table_names[1]}' created in Cassandra database"
    )

    session.execute(
        f"CREATE TABLE IF NOT EXISTS {DB_SETTINGS.db_name}.{DB_SETTINGS.db_table_names[2]} ("
        "film_id int,"
        "id_name text PRIMARY KEY,"
        ")"
    )

    logger.info(
        f"Table '{DB_SETTINGS.db_table_names[2]}' created in Cassandra database"
    )

    session.execute(
        f"CREATE TABLE IF NOT EXISTS {DB_SETTINGS.db_name}.{DB_SETTINGS.db_table_names[3]} ("
        "time_id int,"
        "id_name text PRIMARY KEY,"
        ")"
    )

    logger.info(
        f"Table '{DB_SETTINGS.db_table_names[3]}' created in Cassandra database"
    )


def drop_keyspace(session):
    session.execute(f"DROP KEYSPACE IF EXISTS {DB_SETTINGS.db_name}")
    logger.info(f"Keyspace '{DB_SETTINGS.db_name}' in Cassandra database dropped")


def drop_tables(session):
    session.execute(
        f"DROP TABLE IF EXISTS {DB_SETTINGS.db_name}.{DB_SETTINGS.db_table_names[0]}"
    )
    logger.info(
        f"Table '{DB_SETTINGS.db_table_names[0]}' in Cassandra database dropped"
    )

    session.execute(
        f"DROP TABLE IF EXISTS {DB_SETTINGS.db_name}.{DB_SETTINGS.db_table_names[1]}"
    )
    logger.info(
        f"Table '{DB_SETTINGS.db_table_names[1]}' in Cassandra database dropped"
    )

    session.execute(
        f"DROP TABLE IF EXISTS {DB_SETTINGS.db_name}.{DB_SETTINGS.db_table_names[2]}"
    )
    logger.info(
        f"Table '{DB_SETTINGS.db_table_names[2]}' in Cassandra database dropped"
    )

    session.execute(
        f"DROP TABLE IF EXISTS {DB_SETTINGS.db_name}.{DB_SETTINGS.db_table_names[3]}"
    )
    logger.info(
        f"Table '{DB_SETTINGS.db_table_names[3]}' in Cassandra database dropped"
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


def cleanup_cassandra_db():
    session = set_db_connection()

    drop_tables(session)
    drop_keyspace(session)

    session.shutdown()

    logger.info("Cassandra database cleaned up")


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


def get_table_sizes(keyspace):
    session = set_db_connection()

    table_sizes = {}

    # Retrieve a list of all tables in the keyspace
    tables = session.execute(
        f"SELECT table_name FROM system_schema.tables WHERE keyspace_name = '{keyspace}'",
    )

    for table in tables:
        table_name = table.table_name
        # Execute a query to retrieve the size of data in the table
        result = session.execute(
            f"SELECT sum(partitions_count) as size FROM system.size_estimates WHERE keyspace_name = '{keyspace}' AND table_name = '{table_name}'"
        )
        size = result.one().size
        table_sizes[table_name] = size

    session.shutdown()

    return table_sizes


def check_table_sizes():
    keyspace = DB_SETTINGS.db_name

    tables_details = []

    sizes = get_table_sizes(keyspace)
    for table, size in sizes.items():
        size_units = ["bytes", "kB", "mB", "gB"]
        unit_index = 0

        while size >= 1024 and unit_index < len(size_units) - 1:
            size /= 1024
            unit_index += 1

        size = f"{size} {size_units[unit_index]}"

        tab_details = {"name": str(table), "size": size}
        tables_details.append(tab_details)

    logger.info("Table sizes checked")

    return tables_details


def restart_tables():
    cleanup_cassandra_db()
    init_cassandra_db()

    logger.info("Cassandra database tables restarted")
