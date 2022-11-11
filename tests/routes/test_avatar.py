from unittest.mock import Mock
from unittest import IsolatedAsyncioTestCase, main
from functools import partial

from sanic.response import json

from config.db import MongoClient
from routes.avatar import get_by_pet_id
from models.avatar import Avatar
from common.promise import Promise

MongoClient().connect()

class AvatarTests(IsolatedAsyncioTestCase):

    async def test_get_by_pet_id_should_return_404(self) -> None:
        req: Mock = Mock()
        res: json = await get_by_pet_id(req, '636aa321655058ff2d4e1fce')
        self.assertEqual(res.status, 404)

    async def test_get_by_pet_id_should_return_200(self) -> None:
        avatar_dict: dict = {
            'pet_id': '636aa321655058ff2d4e1fce',
            'path': 'profile.png',
        }
        avatar: Avatar = Avatar(**avatar_dict)
        await Promise.resolve(partial(avatar.save))

        req: Mock = Mock()
        res: json = await get_by_pet_id(req, '636aa321655058ff2d4e1fce')

        self.assertEqual(res.status, 200)

        await Promise.resolve(partial(Avatar.objects.delete))


if __name__ == '__main__':
    main()
