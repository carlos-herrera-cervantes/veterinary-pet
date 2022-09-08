from mongoengine import *
from mongoengine import signals

from datetime import datetime


class Avatar(Document):
    pet_id: str = ObjectIdField(required=True)
    path: str = StringField(required=True)
    created_at: datetime = DateTimeField(default=datetime.utcnow())
    updated_at: datetime = DateTimeField(default=datetime.utcnow())
    meta: dict = {'collection': 'avatars'}

    @classmethod
    def pre_save(cls: any, sender: any, document: Document, **kwargs: dict) -> None:
        document.updated_at = datetime.utcnow()


signals.pre_save.connect(Avatar.pre_save, sender=Avatar)
