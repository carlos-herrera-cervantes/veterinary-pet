from json import loads
from functools import partial

from sanic import Blueprint
from sanic.response import json
from sanic.request import Request
from bson.objectid import ObjectId

from models.race import Race
from common.serializer import default
from common.promise import Promise
from decorators.common import validate_body

race_router = Blueprint('race_router')


@race_router.route('/classifications/<classification_pk>/races', methods=['GET'])
async def get_by_classification(_: Request, classification_pk: str) -> json:
    raw_filter = {'classification_id': ObjectId(classification_pk)}
    races = await Promise.resolve(partial(Race.objects, __raw__=raw_filter))
    return json({'data': loads(races.to_json(), object_hook=default)})


@race_router.route('/classifications/<classification_pk>/races', methods=['POST'])
@validate_body
async def create_many(req: Request, classification_pk: str) -> json:
    try:
        body: dict = req.json
        races = [
            Race(**{
                'classification_id': classification_pk,
                'name': obj['name'],
            }) for obj in body
        ]
        await Promise.resolve(partial(Race.objects.insert, races))
        return json({'data': 'ok'}, status=201)
    except Exception as e:
        return json({'message': e}, status=400)


@race_router.route('/classifications/<classification_pk>/races/<race_pk>', methods=['DELETE'])
async def delete_by_id(_: Request, __: str, race_pk: str) -> json:
    races = await Promise.resolve(partial(Race.objects, id=ObjectId(race_pk)))
    await Promise.resolve(partial(races.delete))
    return json({}, status=204)
