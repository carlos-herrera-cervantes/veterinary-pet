from json import loads
from functools import partial

from sanic import Blueprint
from sanic.response import json
from sanic.request import Request
from bson.objectid import ObjectId

from models.classification import Classification
from common.serializer import default
from common.promise import Promise
from decorators.common import validate_body

classification_router = Blueprint('classification_router')


@classification_router.route('/classifications', methods=['GET'])
async def get_all(_: Request) -> json:
    classifications = await Promise.resolve(partial(Classification.objects))
    return json({'data': loads(classifications.to_json(), object_hook=default)})


@classification_router.route('/classifications', methods=['POST'])
@validate_body
async def create_many(req: Request) -> json:
    try:
        body: dict = req.json
        classifications = [Classification(**obj) for obj in body]
        await Promise.resolve(partial(Classification.objects.insert, classifications))
        return json({'data': 'ok'}, status=201)
    except Exception as e:
        return json({'message': e}, status=400)


@classification_router.route('/classifications/<pk>', methods=['DELETE'])
async def delete_by_id(_: Request, pk: str) -> json:
    classification = await Promise.resolve(partial(Classification.objects, id=ObjectId(pk)))
    await Promise.resolve(classification.delete)
    return json({}, status=204)
