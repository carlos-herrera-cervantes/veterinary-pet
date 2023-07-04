import logging
from json import loads
from functools import partial

from sanic.response import json
from sanic import Blueprint
from sanic.request import Request
from bson.objectid import ObjectId

from common.serializer import default
from common.promise import Promise
from decorators.avatar import validate_image
from models.avatar import Avatar
from config.app import AwsS3Config
from config.aws import Aws

avatar_router = Blueprint('avatar_router')
logger = logging.getLogger(__name__)
logger_path = '[routes][avatar.py]'


@avatar_router.route('/<pk>/avatar', methods=['GET'])
async def get_by_pet_id(_: Request, pk: str) -> json:
    try:
        avatar: Avatar = await Promise.resolve(partial(Avatar.objects.get, __raw__={'pet_id': ObjectId(pk)}))
        avatar.path = (
            AwsS3Config.AVATAR_S3_ENDPOINT.value + '/' +
            AwsS3Config.AVATAR_S3.value + '/' + avatar.path
        )

        return json({'data': loads(avatar.to_json(), object_hook=default)})
    except Exception as e:
        logger.error(f'{logger_path}[get_by_pet_id][{e}]')
        return json({'message': 'not found'}, status=404)


@avatar_router.route('/<pk>/avatar', methods=['POST'])
@validate_image
async def upsert(req: Request, pk: str) -> json:
    image = req.files.get('image')
    key = f'{pk}/{image.name}'
    s3_client = Aws().get_s3_client()
    bucket = s3_client.Bucket(AwsS3Config.AVATAR_S3.value)

    [avatar, _] = await Promise.resolve_all([
        partial(Avatar.objects, __raw__={'pet_id': ObjectId(pk)}),
        partial(bucket.put_object, Key=key, Body=image.body),
    ])

    if not avatar:
        new_avatar = Avatar(**{'pet_id': pk, 'path': key})
        avatar = await Promise.resolve(partial(new_avatar.save))
    else:
        s3_object = s3_client.Object(AwsS3Config.AVATAR_S3.value, avatar[0].path)
        await Promise.resolve_all([
            partial(s3_object.delete),
            partial(avatar.update_one, **{'path': key}),
        ])

        avatar = await Promise.resolve(
            partial(Avatar.objects.get, __raw__={'pet_id': ObjectId(pk)}),
        )
        await Promise.resolve(partial(avatar.save))

    avatar['path'] = (
        AwsS3Config.AVATAR_S3_ENDPOINT.value + '/' +
        AwsS3Config.AVATAR_S3.value + '/' + key
    )

    return json({
        'data': loads(avatar.to_json(), object_hook=default)
    }, status=201)


@avatar_router.route('/<pk>/avatar', methods=['DELETE'])
async def delete_by_pet_id(_: Request, pk: str) -> json:
    try:
        s3_client = Aws().get_s3_client()
        avatar: Avatar = await Promise.resolve(
            partial(Avatar.objects.get, __raw__={'pet_id': ObjectId(pk)}),
        )
        s3_object = s3_client.Object(AwsS3Config.AVATAR_S3.value, avatar.path)

        await Promise.resolve_all([
            partial(s3_object.delete),
            partial(avatar.delete),
        ])

        return json({}, status=204)
    except Exception as e:
        logger.error(f'{logger_path}[delete_by_pet_id][{e}]')
        return json({'message': 'not found'}, status=404)
