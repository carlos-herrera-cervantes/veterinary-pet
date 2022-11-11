from unittest.mock import Mock
from unittest import IsolatedAsyncioTestCase, main
from functools import partial
from json import loads

from sanic.response import json
from bson.objectid import ObjectId

from config.db import MongoClient
from models.profile import Profile
from common.promise import Promise
from routes.profile import get_all, get_by_customer_id, get_me, create, update, delete_by_id

MongoClient().connect()

class ProfileTests(IsolatedAsyncioTestCase):

    async def test_get_all_should_return_200(self) -> None:
        req: Mock = Mock()
        res: json = await get_all(req)
        body: dict = loads(res.body)

        self.assertEqual(res.status, 200)
        self.assertEqual(len(body['data']), 0)

    async def test_get_by_customer_id_should_return_200(self) -> None:
        req: Mock = Mock()
        res: json = await get_by_customer_id(req, '636b06207abfba54fd2551f5')
        body: dict = loads(res.body)

        self.assertEqual(res.status, 200)
        self.assertEqual(len(body['data']), 0)

    async def test_get_me_should_return_403(self) -> None:
        req: Mock = Mock()
        req.headers = {}
        res: json = await get_me(req)

        self.assertEqual(res.status, 403)

    async def test_get_me_should_return_200(self) -> None:
        req: Mock = Mock()
        req.headers = { 'user-id': '636b06207abfba54fd2551f5' }
        res: json = await get_me(req)
        body: dict = loads(res.body)

        self.assertEqual(res.status, 200)
        self.assertEqual(len(body['data']), 0)

    async def test_create_should_return_201(self) -> None:
        req: Mock = Mock()
        req.headers = { 'user-id': '636b06207abfba54fd2551f5' }
        req.json = {
            'color': 'Brown',
            'name': 'Miguel',
            'birthday': '2010-01-01',
            'race_id': '636da8caf670fc41a23136e4',
            'classification_id': '636da8e4a2a711083582ff15',
        }
        res: json = await create(req)

        self.assertEqual(res.status, 201)

        await Promise.resolve(partial(Profile.objects.delete))

    async def test_update_should_return_200(self) -> None:
        profile_dict: dict = {
            'customer_id': '636b06207abfba54fd2551f5',
            'color': 'Brown',
            'name': 'Miguel',
            'birthday': '2010-01-01',
            'race_id': '636da8caf670fc41a23136e4',
            'classification_id': '636da8e4a2a711083582ff15',
        }
        profile: Profile = Profile(**profile_dict)
        insertResult: Profile = await Promise.resolve(partial(profile.save))

        req: Mock = Mock()
        req.json = { 'color': 'Blue' }
        res: json = await update(req, insertResult.pk)

        self.assertEqual(res.status, 200)

        getResult: Profile = await Promise.resolve(
            partial(Profile.objects.get, id=ObjectId(insertResult.pk))
        )

        self.assertEqual(getResult.color, 'Blue')

        await Promise.resolve(partial(Profile.objects.delete))

    async def test_delete_by_id_should_return_204(self) -> None:
        profile_dict: dict = {
            'customer_id': '636b06207abfba54fd2551f5',
            'color': 'Brown',
            'name': 'Miguel',
            'birthday': '2010-01-01',
            'race_id': '636da8caf670fc41a23136e4',
            'classification_id': '636da8e4a2a711083582ff15',
        }
        profile: Profile = Profile(**profile_dict)
        insertResult: Profile = await Promise.resolve(partial(profile.save))

        req: Mock = Mock()
        res: json = await delete_by_id(req, insertResult.pk)

        self.assertEqual(res.status, 204)

        await Promise.resolve(partial(Profile.objects.delete))


if __name__ == '__main__':
    main()
