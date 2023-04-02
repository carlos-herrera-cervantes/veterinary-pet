from sanic import Sanic, Blueprint
from sanic.response import json
from sanic.request import Request

from config.db import MongoClient
from config.app import AppConfig, ApiConfig
from routes.profile import profile_router
from routes.allergy import allergy_router
from routes.classification import classification_router
from routes.race import race_router
from routes.avatar import avatar_router

MongoClient().connect()
app = Sanic('veterinary-pet')

v1 = Blueprint.group(
    profile_router,
    allergy_router,
    classification_router,
    race_router,
    avatar_router,
    url_prefix=f'{ApiConfig.BASE_PATH.value}/v1',
)
app.blueprint(v1)


@app.route('/')
async def health_check(req: Request) -> json:
    return json({
        'status': True,
        'message': 'Server is up'
    })

if __name__ == '__main__':
    app.run(
        host=AppConfig.HOST.value,
        port=AppConfig.PORT.value,
        debug=True,
    )
