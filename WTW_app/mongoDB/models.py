from mongoengine import (
    Document,
    SequenceField,
    StringField,
    IntField,
    FloatField,
    EmbeddedDocument,
    EmbeddedDocumentField,
)


class Details(EmbeddedDocument):
    """Embedded document for film details."""

    director = StringField(required=True)
    description = StringField(required=True)


class Film(Document):
    """Model for the Films collection."""

    film_id = SequenceField(primary_key=True)
    title = StringField(required=True)
    year = IntField(required=True)
    rate = FloatField(required=True)
    img_url = StringField()
    details = EmbeddedDocumentField(Details)

    meta = {"collection": "films"}


class Times(Document):
    """Model for the Times collection."""

    time_id = SequenceField(primary_key=True)
    database = StringField(required=True)
    request_type = StringField(required=True)
    time_value = FloatField(required=True)

    meta = {"collection": "times"}
