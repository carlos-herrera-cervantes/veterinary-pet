from unittest.mock import Mock
from unittest import IsolatedAsyncioTestCase, main
from functools import partial
from json import loads

from sanic.response import json

from config.db import MongoClient
from models.classification import Classification
from common.promise import Promise
from routes.classification import get_all, create_many, delete_by_id

MongoClient().connect()

class ClassificationTests(IsolatedAsyncioTestCase):

    async def test_get_all_should_return_200(self) -> None:
        req: Mock = Mock()
        res: json = await get_all(req)
        body: dict = loads(res.body)

        self.assertEqual(res.status, 200)
        self.assertEqual(len(body['data']), 0)

    async def test_create_many_should_return_201(self) -> None:
        req: Mock = Mock()
        req.json = [
            {
                'name': 'Cat',
            },
            {
                'name': 'Dog',
            }
        ]
        res: json = await create_many(req)
        counter: int = await Promise.resolve(partial(Classification.objects.count))

        self.assertEqual(res.status, 201)
        self.assertEqual(counter, 2)

        await Promise.resolve(partial(Classification.objects.delete))

    async def test_delete_by_id_should_return_204(self) -> None:
        classification_dict: dict = { 'name': 'Dog' }
        classification: Classification = Classification(**classification_dict)
        insertResult: Classification = await Promise.resolve(partial(classification.save))

        req: Mock = Mock()
        res: json = await delete_by_id(req, insertResult.pk)
        counter: int = await Promise.resolve(partial(Classification.objects.count))

        self.assertEqual(res.status, 204)
        self.assertEqual(counter, 0)


if __name__ == '__main__':
    main()
