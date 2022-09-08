from functools import wraps
from typing import Callable

from sanic.response import json
from sanic.request import Request


def validate_body(fn: Callable) -> Callable:
    @wraps(fn)
    def inner_fn(req: Request, *args: dict, **kwargs: dict) -> json:
        body: dict = req.json
        
        if not body:
            return json({'message': 'Invalid body'}, status=400)

        return fn(req, *args, **kwargs)
    return inner_fn
