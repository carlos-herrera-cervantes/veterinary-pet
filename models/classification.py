from mongoengine import *

from datetime import datetime


class Classification(Document):
    name: str = StringField(required=True)
    created_at: datetime = DateTimeField(default=datetime.utcnow())
    updated_at: datetime = DateTimeField(default=datetime.utcnow())
    meta: dict = {'collection': 'classifications'}
