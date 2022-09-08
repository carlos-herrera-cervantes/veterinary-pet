from datetime import datetime
from mongoengine import Document


def default(document: Document) -> Document:
    if '_id' in document.keys():
        document['id'] = document['_id']['$oid']

    if 'customer_id' in document.keys():
        document['customer_id'] = document['customer_id']['$oid']

    if 'pet_id' in document.keys():
        document['pet_id'] = document['pet_id']['$oid']

    if 'classification_id' in document.keys():
        document['classification_id'] = document['classification_id']['$oid']

    if 'created_at' in document.keys():
        document['created_at'] = datetime.fromtimestamp(document['created_at']['$date'] / 1000).isoformat()
        document['updated_at'] = datetime.fromtimestamp(document['updated_at']['$date'] / 1000).isoformat()

    if 'birthday' in document.keys():
        document['birthday'] = datetime.fromtimestamp(document['birthday']['$date'] / 1000).isoformat()

    document.pop('_id', None)
    document.pop('password', None)

    return document
