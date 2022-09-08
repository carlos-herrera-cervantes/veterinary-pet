from functools import wraps
from typing import Callable

from sanic.response import json
from sanic.request import Request


def validate_race(fn: Callable) -> Callable:
    @wraps(fn)
    def inner_fn(req: Request, *args: dict, **kwargs: dict) -> json:
        body: list[any] = req.json

        if type(body) is not list:
            return json({'message': 'The body should be list'}, status=400)

        fields: list[str] = ['name']
        name: str = body.get('name', None)

        if name:
            return fn(req, *args, **kwargs)

        message: str = (
            'Missing fields.' +
            'The body must have the following properties: ' +
            ','.join(fields)
        )

        return json({'message': message}, status=400)
    return inner_fn
