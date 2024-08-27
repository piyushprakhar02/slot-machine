import boto3
from decouple import config

USER_POOL_ID = config('AWS_COGNITO_USER_POOL_ID')
CLIENT_ID = config('AWS_COGNITO_CLIENT_ID')
REGION = config('AWS_REGION')

# Initialize SQS Client
sqs_client = boto3.client('sqs', region_name='us-east-1')


def get_sqs_client():
    return sqs_client
