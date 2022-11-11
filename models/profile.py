from datetime import datetime, date

from mongoengine import *
from mongoengine import signals

from enums.gender import Gender

def validate_name(name: str) -> None | ValidationError:
    if len(name):
        return

    raise ValidationError('Name should not be empty')

def validate_birthday(birthday: str) -> None | ValidationError:
    if birthday:
        return

    raise ValidationError('Birthday should not be empty')

def validate_race_id(race_id: str) -> None | ValidationError:
    if race_id:
        return

    raise ValidationError('Race should not be empty')

def validate_classification_id(classification_id: str) -> None | ValidationError:
    if classification_id:
        return

    raise ValidationError('Classification should not be empty')

def validate_customer_id(customer_id: str) -> None | ValidationError:
    if customer_id:
        return

    raise ValidationError('Customer id should not be empty')


class Profile(Document):
    customer_id: str = ObjectIdField(required=True, validation=validate_customer_id)
    color: str = StringField()
    name: str = StringField(required=True, validation=validate_name)
    birthday: date = DateField(required=True, validation=validate_birthday)
    race_id: str = ObjectIdField(required=True, validation=validate_race_id)
    classification_id: str = ObjectIdField(required=True, validation=validate_classification_id)
    gender: str = StringField(default=Gender.NOT_SPECIFIED.value)
    created_at: datetime = DateTimeField(default=datetime.utcnow())
    updated_at: datetime = DateTimeField(default=datetime.utcnow())
    meta: dict = {'collection': 'profiles'}

    @classmethod
    def pre_save(cls: any, sender: any, document: Document, **kwargs: dict) -> None:
        document.updated_at = datetime.utcnow()


signals.pre_save.connect(Profile.pre_save, sender=Profile)
