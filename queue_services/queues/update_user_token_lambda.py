import json
from constant import Constant
from services.user_token_service import UserTokenService
from database import getDBSession


def handler(event, context):
    session = getDBSession()
    try:
        for record in event['Records']:
            message_body = record['body']
            message_data = json.loads(message_body)
            print(f"Processing message: {message_data}")

            user_id = message_data['user_id']
            transaction_type = message_data['transaction_type']
            transaction_amount = message_data['transaction_amount']

            if transaction_type == Constant.TOKEN_CREDIT:
                user_token = UserTokenService(user_id=user_id, db=session)
                user_token.credit_balance(amount=transaction_amount)

            elif transaction_type == Constant.TOKEN_DEBIT:
                user_token = UserTokenService(user_id=user_id, db=session)
                user_token.debit_balance(amount=transaction_amount)

    except Exception as e:
        print(f"Error processing messages: {e}")
