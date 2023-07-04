import boto3

from common.singleton import SingletonMeta
from config.app import AwsS3Config


class Aws(metaclass=SingletonMeta):

    def __init__(self) -> None:
        self.__s3_endpoint = AwsS3Config.AVATAR_S3_ENDPOINT.value
        self.__s3_region = AwsS3Config.AVATAR_S3_REGION.value

    def get_s3_client(self) -> any:
        client = boto3.resource(
            's3',
            region_name=self.__s3_region,
            endpoint_url=self.__s3_endpoint,
        )
        return client
