from functools import wraps
from typing import Callable

from sanic.response import json
from sanic.request import Request


def validate_classification(fn: Callable) -> Callable:
    @wraps(fn)
    def inner_fn(req: Request, *args: dict, **kwargs: dict) -> json:
        body: list[any] = req.json

        if type(body) is not list:
            return json({'message': 'The body should be list'}, status=400)

        fields: list[str] = ['name']
        message: str = (
            'Missing fields.' +
            'The objects must have the following properties: ' +
            ','.join(fields)
        )

        for obj in body:
            if obj.get('name', None):
                continue

            return json({'message': message}, status=400)

        return fn(req, *args, **kwargs)
    return inner_fn
