import json

from utils.sns_utils import get_sns_client
from decouple import config

USER_TOKEN_UPDATE_SNS_TOPIC_ARN = config('USER_TOKEN_UPDATE_SNS_TOPIC_ARN')


class SnsService:

    def publish(self, message_body: dict):
        try:
            sns_client = get_sns_client()
            response = sns_client.publish(
                TopicArn=USER_TOKEN_UPDATE_SNS_TOPIC_ARN,
                Subject='User Token Update',
                Message=json.dumps(message_body),
                MessageAttributes={
                    "event_type": {
                        "DataType": "String",
                        "StringValue": "update-token-balance"
                    }
                }
            )
            return response

        except Exception as e:
            print(e)
