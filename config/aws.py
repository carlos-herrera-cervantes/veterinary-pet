import boto3

from common.singleton import SingletonMeta
from config.app import S3 as S3Config


class S3(metaclass=SingletonMeta):

    def __init__(self) -> None:
        self.__s3_endpoint = S3Config.AVATAR_S3_ENDPOINT.value
        self.__s3_region = S3Config.AVATAR_S3_REGION.value

    def get_client(self) -> any:
        client = boto3.resource(
            's3',
            region_name=self.__s3_region,
            endpoint_url=self.__s3_endpoint,
        )
        return client
