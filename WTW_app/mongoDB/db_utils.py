import logging

from WTW_app.mongoDB.settings.db_settings import DB_SETTINGS

from pymongo import MongoClient
from mongoengine import connect

logger = logging.getLogger()


def set_db_connection():
    client = MongoClient(
        host=DB_SETTINGS.db_host,
        port=int(DB_SETTINGS.db_port),
        authSource=DB_SETTINGS.db_name,
    )

    return client


def init_mongo_db():
    connect(
        db=DB_SETTINGS.db_name,
        host=DB_SETTINGS.db_host,
        port=int(DB_SETTINGS.db_port),
        authentication_source=DB_SETTINGS.db_name,
    )

    client = set_db_connection()

    db_names = client.list_database_names()

    if DB_SETTINGS.db_name not in db_names:
        logger.info("Creating the MongoDB database")

        new_db = client[f"{DB_SETTINGS.db_name}"]

        collections = new_db.list_collection_names()

        if "films" not in collections:
            logger.info("Creating the films collection")
            new_db.create_collection("films")

        if "times" not in collections:
            logger.info("Creating the times collection")
            new_db.create_collection("times")

    logger.info("MongoDB database started")


def check_db_status():
    db_state = "Error"

    client = set_db_connection()

    db_names = client.list_database_names()

    if DB_SETTINGS.db_name in db_names:
        db_state = "Started"

        db = client[f"{DB_SETTINGS.db_name}"]

        collections = db.list_collection_names()

        if "films" not in collections:
            db_state = "Error"

        if "times" not in collections:
            db_state = "Error"

    return db_state


def get_collections_size():
    client = set_db_connection()
    db = client[f"{DB_SETTINGS.db_name}"]

    collections_details = []

    collections = db.list_collection_names()
    for collection_name in collections:
        collection_stats = db.command("collstats", collection_name)

        size_in_bytes = collection_stats["storageSize"]

        size_units = ["bytes", "kB", "mB", "gB"]
        size = size_in_bytes
        unit_index = 0

        while size >= 1024 and unit_index < len(size_units) - 1:
            size /= 1024
            unit_index += 1

        coll_size = f"{size} {size_units[unit_index]}"

        coll_details = {"name": str(collection_name), "size": coll_size}
        collections_details.append(coll_details)

    return collections_details


def restart_collections():
    client = set_db_connection()
    db = client[f"{DB_SETTINGS.db_name}"]

    collections = db.list_collection_names()

    for collection in collections:
        db.drop_collection(collection)
        db.create_collection(collection)

    logger.info("MongoDB database collections restarted")
