from functools import wraps
from typing import Callable

from sanic.response import json
from sanic.request import Request


def validate_image(fn: Callable) -> Callable:
    @wraps(fn)
    def inner_fn(req: Request, *args: dict, **kwargs: dict) -> json:
        image: any = req.files.get('image')

        if not image:
            return json({'message': 'invalid image'}, status=400)

        return fn(req, *args, **kwargs)
    return inner_fn
