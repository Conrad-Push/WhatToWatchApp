from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Film(Model):
    film_id = columns.UUID(primary_key=True)
    title = columns.Text()
    year = columns.Integer()
    rate = columns.Float()
    img_url = columns.Text()
    details = columns.Map(columns.Text(), columns.Text())


class Times(Model):
    time_id = columns.UUID(primary_key=True)
    database = columns.Text()
    request_type = columns.Text()
    time_value = columns.Float()
