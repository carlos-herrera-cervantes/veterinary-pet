from unittest.mock import Mock
from unittest import IsolatedAsyncioTestCase, main
from json import loads
from functools import partial

from sanic.response import json

from config.db import MongoClient
from routes.race import get_by_classification, create_many, delete_by_id
from common.promise import Promise
from models.race import Race

MongoClient().connect()

class RaceTests(IsolatedAsyncioTestCase):

    async def test_get_by_classification_should_return_200(self) -> None:
        req: Mock = Mock()
        res: json = await get_by_classification(req, '636d9a820f20fb3807ef5fb0')
        body: dict = loads(res.body)

        self.assertEqual(res.status, 200)
        self.assertEqual(len(body['data']), 0)

    async def test_create_many_should_return_201(self) -> None:
        req: Mock = Mock()
        req.json = [{ 'name': 'Siberian' }, { 'name': 'Classic' }]
        res: json = await create_many(req, '636d9a820f20fb3807ef5fb0')

        self.assertEqual(res.status, 201)

        counter: int = await Promise.resolve(partial(Race.objects.count))

        self.assertEqual(counter, 2)

        await Promise.resolve(partial(Race.objects.delete))

    async def test_delete_by_id_should_return_204(self) -> None:
        race_dict: dict = {
            'classification_id': '636d9a820f20fb3807ef5fb0',
            'name': 'Siberian',
        }
        race: Race = Race(**race_dict)
        insertResult: Race = await Promise.resolve(partial(race.save))

        req: Mock = Mock()
        res: json = await delete_by_id(req, '636d9a820f20fb3807ef5fb0', insertResult.pk)

        self.assertEqual(res.status, 204)

        counter: int = await Promise.resolve(partial(Race.objects.delete))

        self.assertEqual(counter, 0)


if __name__ == '__main__':
    main()
