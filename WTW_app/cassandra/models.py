from WTW_app.cassandra.db_utils import set_db_connection
from WTW_app.cassandra.settings.db_settings import DB_SETTINGS

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.connection import register_connection, set_default_connection


_session = set_db_connection()
register_connection(str(_session), session=_session)
set_default_connection(str(_session))


class Films(Model):
    __keyspace__ = DB_SETTINGS.db_name

    session = _session
    session.default_fetch_size = 1000

    film_id = columns.Integer(primary_key=True)
    title = columns.Text()
    year = columns.Integer()
    rate = columns.Float()
    img_url = columns.Text()
    details = columns.Map(columns.Text(), columns.Text())


class Times(Model):
    __keyspace__ = DB_SETTINGS.db_name

    session = _session
    session.default_fetch_size = 1000

    time_id = columns.Integer(primary_key=True)
    database = columns.Text()
    request_type = columns.Text()
    time_value = columns.Float()


class Film_Id(Model):
    __keyspace__ = DB_SETTINGS.db_name

    session = _session
    session.default_fetch_size = 1000

    film_id = columns.Integer()
    id_name = columns.Text(primary_key=True)


class Time_Id(Model):
    __keyspace__ = DB_SETTINGS.db_name

    session = _session
    session.default_fetch_size = 1000

    time_id = columns.Integer()
    id_name = columns.Text(primary_key=True)
