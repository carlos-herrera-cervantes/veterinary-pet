from mongoengine import *

from datetime import datetime

def validate_name(name: str) -> None | ValidationError:
    if len(name):
        return

    raise ValidationError('Name should not be empty')

def validate_classification_id(classification_id: str) -> None | ValidationError:
    if classification_id:
        return

    raise ValidationError('Classification id should not be empty')


class Race(Document):
    classification_id: str = ObjectIdField(required=True, validation=validate_classification_id)
    name: str = StringField(required=True, validation=validate_name)
    created_at: datetime = DateTimeField(default=datetime.utcnow())
    updated_at: datetime = DateTimeField(default=datetime.utcnow())
    meta: dict = {'collection': 'races'}
