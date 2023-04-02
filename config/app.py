import os
from enum import Enum


class AppConfig(Enum):
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')


class MongoDB(Enum):
    DEFAULT_DB = os.getenv("MONGO_DB_DEFAULT")


class S3(Enum):
    AVATAR_S3 = os.getenv('AVATAR_BUCKET')
    AVATAR_S3_ENDPOINT = os.getenv('AVATAR_S3_ENDPOINT')
    AVATAR_S3_REGION = os.getenv('AVATAR_S3_REGION')


class ApiConfig(Enum):
    BASE_PATH = '/api/veterinary-pet'
