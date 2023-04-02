from json import loads
from functools import partial

from sanic import Blueprint
from sanic.response import json
from sanic.request import Request
from bson.objectid import ObjectId

from models.allergy import Allergy
from common.serializer import default
from common.promise import Promise
from decorators.common import validate_body

allergy_router = Blueprint('allergy_router')
promise = Promise()


@allergy_router.route('/<pet_pk>/allergies', methods=['GET'])
async def get_by_pet(req: Request, pet_pk: str) -> json:
    allergies: list[Allergy] = await promise.resolve(
        partial(Allergy.objects, __raw__={'pet_id': ObjectId(pet_pk)}),
    )
    return json({'data': loads(allergies.to_json(), object_hook=default)})


@allergy_router.route('/<pet_pk>/allergies', methods=['POST'])
@validate_body
async def create(req: Request, pet_pk: str) -> json:
    try:
        body: dict = req.json
        body['pet_id'] = pet_pk

        allergy: Allergy = Allergy(**body)
        created: dict = await promise.resolve(partial(allergy.save))

        return json({'data': loads(created.to_json(), object_hook=default)}, status=201)
    except Exception as e:
        return json({'message': e}, status=400)


@allergy_router.route('/<pet_pk>/allergies/<allergy_pk>', methods=['DELETE'])
async def delete_by_pet(req: Request, pet_pk: str, allergy_pk: str) -> json:
    allergies: list[Allergy] = await promise.resolve(
        partial(
            Allergy.objects,
            __raw__={'pet_id': ObjectId(pet_pk), '_id': ObjectId(allergy_pk)},
        ),
    )
    await promise.resolve(allergies.delete)

    return json({}, status=204)
