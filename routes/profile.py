from json import loads
from functools import partial

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
promise = Promise()


@profile_router.route('/profiles', methods=['GET'])
async def get_all(req: Request) -> json:
    profiles: list[Profile] = await promise.resolve(partial(Profile.objects))
    return json({'data': loads(profiles.to_json(), object_hook=default)})


@profile_router.route('/profiles/<pk>', methods=['GET'])
async def get_by_customer_id(req: Request, pk: str) -> json:
    profiles: list[Profile] = await promise.resolve(
        partial(Profile.objects, __raw__={'customer_id': ObjectId(pk)}),
    )
    return json({'data': loads(profiles.to_json(), object_hook=default)})

@profile_router.route('/profiles/me', methods=['GET'])
async def get_me(req: Request) -> json:
    user_id: str = req.headers.get('user-id', None)

    if not user_id:
        return json({'message': 'Invalid user ID'}, status=403)

    profiles: list[Profile] = await promise.resolve(
        partial(Profile.objects, __raw__={'customer_id': ObjectId(user_id)}),
    )
    return json({'data': loads(profiles.to_json(), object_hook=default)})


@profile_router.route('/profiles', methods=['POST'])
@validate_body
@inject_customer
async def create(req: Request) -> json:
    try:
        body: dict = req.json
        profile: Profile = Profile(**body)
        created: Profile = await promise.resolve(partial(profile.save))
        return json({
            'data': loads(created.to_json(), object_hook=default),
        }, status=201)
    except Exception as e:
        return json({'message': e}, status=400)


@profile_router.route('/profiles/<pk>', methods=['PATCH'])
@validate_body
@debug_body
async def update(req: Request, pk: str) -> json:
    body: dict = req.json

    profiles: list[Profile] = await promise.resolve(
        partial(Profile.objects, id=ObjectId(pk)),
    )
    await promise.resolve(partial(profiles.update_one, **body))

    profile: Profile = await promise.resolve(
        partial(Profile.objects.get, id=ObjectId(pk)),
    )
    await promise.resolve(partial(profile.save))

    return json({'data': loads(profile.to_json(), object_hook=default)})


@profile_router.route('/profiles/<pk>', methods=['DELETE'])
async def delete_by_id(req: Request, pk: str) -> json:
    profiles: list[Profile] = await promise.resolve(
        partial(Profile.objects, id=ObjectId(pk)),
    )
    await promise.resolve(partial(profiles.delete))
    return json({}, status=204)
