from functools import wraps
from typing import Callable

from sanic.response import json
from sanic.request import Request


def inject_customer(fn: Callable) -> Callable:
    @wraps(fn)
    def inner_fn(req: Request, *args: dict, **kwargs: dict) -> json:
        user_id: str = req.headers.get('user-id')

        if not user_id:
            return json({'message': 'Invalid user ID'}, status=400)

        req.json['customer_id'] = user_id

        return fn(req, *args, **kwargs)
    return inner_fn


def debug_body(fn: Callable) -> Callable:
    @wraps(fn)
    def inner_fn(req: Request, *args: dict, **kwargs: dict) -> json:
        req.json.pop('customer_id', None)
        req.json.pop('created_at', None)
        req.json.pop('updated_at', None)
        req.json.pop('id', None)

        return fn(req, *args, **kwargs)
    return inner_fn
