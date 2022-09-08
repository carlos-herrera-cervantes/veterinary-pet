from functools import wraps
from typing import Callable

from sanic.response import json
from sanic.request import Request


def validate_allergy(fn: Callable) -> Callable:
    @wraps(fn)
    def inner_fn(req: Request, *args: dict, **kwargs: dict) -> json:
        body: dict = req.json
        fields: list[str] = [
            'name',
            'description',
        ]

        name: str = body.get('name', None)
        description: str = body.get('description', None)

        if name and description:
            return fn(req, *args, **kwargs)

        message: str = (
            'Missing fields.' +
            'The body must have the following properties: ' +
            ','.join(fields)
        )

        return json({'message': message}, status=400)
    return inner_fn
