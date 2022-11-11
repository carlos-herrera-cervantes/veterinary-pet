from mongoengine import *

from datetime import datetime

def validate_name(name: str) -> None | ValidationError:
    if len(name):
        return

    raise ValidationError('Name should not be empty')

def validate_description(description: str) -> None | ValidationError:
    if len(description):
        return
    
    raise ValidationError('Description should not be empty')

def validate_pet_id(pet_id: str) -> None | ValidationError:
    if pet_id:
        return

    raise ValidationError('Pet id should not be empty')


class Allergy(Document):
    pet_id: str = ObjectIdField(required=True, validation=validate_pet_id)
    name: str = StringField(required=True, validation=validate_name)
    description: str = StringField(required=True, validation=validate_description)
    created_at: datetime = DateTimeField(default=datetime.utcnow())
    updated_at: datetime = DateTimeField(default=datetime.utcnow())
    meta: dict = {'collection': 'allergies'}
