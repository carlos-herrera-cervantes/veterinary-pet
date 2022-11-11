from mongoengine import *

from datetime import datetime

def validate_name(name: str) -> None | ValidationError:
    if len(name):
        return

    raise ValidationError('Name should not be empty')


class Classification(Document):
    name: str = StringField(required=True, validation=validate_name)
    created_at: datetime = DateTimeField(default=datetime.utcnow())
    updated_at: datetime = DateTimeField(default=datetime.utcnow())
    meta: dict = {'collection': 'classifications'}
