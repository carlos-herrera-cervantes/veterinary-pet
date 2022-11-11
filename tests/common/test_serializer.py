from unittest import TestCase, main

from models.profile import Profile
from common.serializer import default


class SerializerTests(TestCase):

    def test_default_should_return_serialized_document(self) -> None:
        profile_dict: dict = {
            'customer_id': { '$oid': '636a80212342d3513ad1733e' },
            'color': 'black',
            'name': 'Miguel',
            'birthday': { '$date': 1667925679 },
            'race': 'Siberian',
            'classification': 'Cat',
        }
        serialized_profile: Profile = default(profile_dict)

        self.assertEqual(serialized_profile['customer_id'], '636a80212342d3513ad1733e')


if __name__ == '__main__':
    main()
