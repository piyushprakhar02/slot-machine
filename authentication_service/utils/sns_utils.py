import boto3
from decouple import config

REGION = config('AWS_REGION')


def get_sns_client():
    return boto3.client('sns', region_name=REGION)
