from unittest.mock import Mock
from unittest import IsolatedAsyncioTestCase, main
from json import loads
from functools import partial

from sanic.response import json

from config.db import MongoClient
from routes.allergy import get_by_pet, create, delete_by_pet
from models.allergy import Allergy
from common.promise import Promise

MongoClient().connect()

class AllergyTests(IsolatedAsyncioTestCase):

    async def test_get_by_pet_should_return_200(self) -> None:
        req: Mock = Mock()
        res: json = await get_by_pet(req, '636aa321655058ff2d4e1fce')
        body: dict = loads(res.body)

        self.assertEqual(res.status, 200)
        self.assertEqual(len(body['data']), 0)

    async def test_create_should_return_201(self) -> None:
        req: Mock = Mock()
        req.json = {
            'name': 'Test allergy',
            'description': 'This is a test',
        }
        res: json = await create(req, '636aa321655058ff2d4e1fce')
        counter: int = await Promise.resolve(partial(Allergy.objects.count))

        self.assertEqual(res.status, 201)
        self.assertEqual(counter, 1)

        await Promise.resolve(partial(Allergy.objects.delete))

    async def test_delete_by_pet_should_return_204(self) -> None:
        reqBeforeDelete: Mock = Mock()
        reqBeforeDelete.json = {
            'name': 'Test allergy',
            'description': 'This is a test',
        }
        pet_id: str = '636aa321655058ff2d4e1fce'

        resBeforeDelete: json = await create(reqBeforeDelete, pet_id)
        counterBeforeDelete: int = await Promise.resolve(partial(Allergy.objects.count))

        self.assertEqual(resBeforeDelete.status, 201)
        self.assertEqual(counterBeforeDelete, 1)

        reqAfterDelete: Mock = Mock()
        body: dict = loads(resBeforeDelete.body)
        allergy_id: str = body.get('data').get('id')

        resAfterDelete: json = await delete_by_pet(reqAfterDelete, pet_id, allergy_id)
        counterAfterDelete: int = await Promise.resolve(partial(Allergy.objects.count))

        self.assertEqual(resAfterDelete.status, 204)
        self.assertEqual(counterAfterDelete, 0)


if __name__ == '__main__':
    main()
