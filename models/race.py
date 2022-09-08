from mongoengine import *

from datetime import datetime


class Race(Document):
    classification_id: str = ObjectIdField(required=True)
    name: str = StringField(required=True)
    created_at: datetime = DateTimeField(default=datetime.utcnow())
    updated_at: datetime = DateTimeField(default=datetime.utcnow())
    meta: dict = {'collection': 'races'}
