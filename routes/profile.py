from json import loads
from functools import partial
import logging

from sanic.response import json
from sanic import Blueprint
from sanic.request import Request
from bson.objectid import ObjectId

from models.profile import Profile
from common.serializer import default
from common.promise import Promise
from decorators.profile import inject_customer, debug_body
from decorators.common import validate_body

profile_router = Blueprint('profile_router')
logger = logging.getLogger(__name__)


@profile_router.route('/profiles', methods=['GET'])
async def get_all(_: Request) -> json:
    profiles = await Promise.resolve(partial(Profile.objects))
    return json({'data': loads(profiles.to_json(), object_hook=default)})


@profile_router.route('/profiles/<pk>', methods=['GET'])
async def get_by_id(_: Request, pk: str) -> json:
    try:
        profile: Profile = await Promise.resolve(partial(Profile.objects.get, id=ObjectId(pk)))
    except Exception as e:
        logger.error(f'Pet profile not found: {e}')
        return json({'message': 'Pet profile not found'}, status=404)

    return json(loads(profile.to_json(), object_hook=default))


@profile_router.route('/profiles/<pk>/customer', methods=['GET'])
async def get_by_customer_id(_: Request, pk: str) -> json:
    profiles = await Promise.resolve(partial(Profile.objects, __raw__={'customer_id': ObjectId(pk)}))
    return json({'data': loads(profiles.to_json(), object_hook=default)})


@profile_router.route('/profiles/me', methods=['GET'])
async def get_me(req: Request) -> json:
    user_id: str = req.headers.get('user-id', None)

    if not user_id:
        return json({'message': 'Invalid user ID'}, status=403)

    profiles = await Promise.resolve(partial(Profile.objects, __raw__={'customer_id': ObjectId(user_id)}))
    return json({'data': loads(profiles.to_json(), object_hook=default)})


@profile_router.route('/profiles/me', methods=['POST'])
@validate_body
@inject_customer
async def create(req: Request) -> json:
    try:
        body: dict = req.json
        profile = Profile(**body)
        created: Profile = await Promise.resolve(partial(profile.save))
        return json({
            'data': loads(created.to_json(), object_hook=default),
        }, status=201)
    except Exception as e:
        return json({'message': e}, status=400)


@profile_router.route('/profiles/<pk>/me', methods=['PATCH'])
@validate_body
@debug_body
async def update(req: Request, pk: str) -> json:
    body: dict = req.json
    profiles = await Promise.resolve(partial(Profile.objects, id=ObjectId(pk)))
    await Promise.resolve(partial(profiles.update_one, **body))

    profile: Profile = await Promise.resolve(partial(Profile.objects.get, id=ObjectId(pk)))
    await Promise.resolve(partial(profile.save))

    return json({'data': loads(profile.to_json(), object_hook=default)})


@profile_router.route('/profiles/<pk>/me', methods=['DELETE'])
async def delete_by_id(_: Request, pk: str) -> json:
    profiles = await Promise.resolve(partial(Profile.objects, id=ObjectId(pk)))
    await Promise.resolve(partial(profiles.delete))
    return json({}, status=204)
