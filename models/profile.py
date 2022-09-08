from datetime import datetime, date

from mongoengine import *
from mongoengine import signals

from enums.gender import Gender


class Profile(Document):
    customer_id: str = ObjectIdField(required=True)
    color: str = StringField()
    name: str = StringField(required=True)
    birthday: date = DateField(required=True)
    race: str = StringField(required=True)
    classification: str = StringField(required=True)
    gender: str = StringField(default=Gender.NOT_SPECIFIED.value)
    created_at: datetime = DateTimeField(default=datetime.utcnow())
    updated_at: datetime = DateTimeField(default=datetime.utcnow())
    meta: dict = {'collection': 'profiles'}

    @classmethod
    def pre_save(cls: any, sender: any, document: Document, **kwargs: dict) -> None:
        document.updated_at = datetime.utcnow()


signals.pre_save.connect(Profile.pre_save, sender=Profile)
