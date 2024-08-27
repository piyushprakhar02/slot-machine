import boto3
from decouple import config

USER_POOL_ID = config('AWS_COGNITO_USER_POOL_ID')
CLIENT_ID = config('AWS_COGNITO_CLIENT_ID')
REGION = config('AWS_REGION')

# Initialize Cognito Client
cognito_client = boto3.client('cognito-idp', region_name=REGION)


def get_cognito_client():
    return cognito_client


def get_cognito_pool_id():
    return USER_POOL_ID


def get_cognito_client_id():
    return CLIENT_ID
