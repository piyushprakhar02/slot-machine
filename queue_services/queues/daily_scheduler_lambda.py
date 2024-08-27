import json
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from services.user_token_service import UserTokenService
from model import User
from database import getDBSession


def handler(event, context):
    """
    AWS Lambda function triggered daily by AWS EventBridge at midnight.

    This function checks for all users who logged in the previous day and credits
    them with an additional token.
    """
    session = getDBSession()

    today = datetime.now()
    start_of_yesterday = today - timedelta(days=1)
    start_of_yesterday = start_of_yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_yesterday = today.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)

    try:
        # Find users who logged in yesterday
        users = session.query(User).filter(User.last_login_at >= start_of_yesterday, User.last_login_at <= end_of_yesterday).all()

        if not users:
            return {
                'statusCode': 200,
                'body': json.dumps('No users found who logged in yesterday.')
            }

        # Update token balance for each user
        for user in users:
            user_token_service = UserTokenService(user_id=user.id, db=session)
            user_token_service.credit_balance(amount=1)

        session.commit()

        return

    except SQLAlchemyError as e:
        session.rollback()
        print(f'SQLAlchemyError: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps('Database error processing request')
        }
    except Exception as e:
        session.rollback()
        print(f'Error: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing request')
        }
    finally:
        session.close()
