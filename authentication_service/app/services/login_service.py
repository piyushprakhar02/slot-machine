from utils.cognito_utils import get_cognito_client
from decouple import config
from app.database import Session
from constant import Constant
from datetime import datetime
from app.schemas.login_schema import UserLoginSchema
from app.repositories.user_repository import UserRepository

CLIENT_ID = config('AWS_COGNITO_CLIENT_ID')


class UserLoginService:
    def __init__(self, db: Session):
        self.db = db

    def login(self, data: UserLoginSchema) -> str:
        cognito_client = get_cognito_client()
        try:
            response = cognito_client.initiate_auth(
                ClientId=CLIENT_ID,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': data.email,
                    'PASSWORD': data.password.get_secret_value(),
                }
            )

            print(f"Response: {response}")

            if not response['ChallengeParameters']:
                user_service = UserRepository(db=self.db)
                user_service.update_user(email=data.email, data={'last_login_at': datetime.utcnow()})
                return {"token": response['AuthenticationResult']['AccessToken']}

            else:
                if response['ChallengeName'] == 'SOFTWARE_TOKEN_MFA':
                    return {"challenge": response}

        except cognito_client.exceptions.NotAuthorizedException:
            raise InvalidCredentialsException()
        except Exception as e:
            print(e)
            raise LoginServiceException()

    def respond_to_mfa_challenge(self, email: str, session: str, code: str):
        try:
            cognito_client = get_cognito_client()
            response = cognito_client.respond_to_auth_challenge(
                ClientId=CLIENT_ID,
                ChallengeName='SOFTWARE_TOKEN_MFA',
                Session=session,
                ChallengeResponses={
                    'USERNAME': email,
                    'SOFTWARE_TOKEN_MFA_CODE': code
                }
            )
            user_service = UserRepository(db=self.db)
            user_service.update_user(email=email, data={'last_login_at': datetime.utcnow()})
            return response["AuthenticationResult"]["AccessToken"]
        except Exception as e:
            print(f"An error occurred: {e}")
            raise


class InvalidCredentialsException(Exception):
    def __init__(self, message=Constant.LOGIN_INVALID_CREDENTIALS_ERROR_MESSAGE):
        self.message = message
        super().__init__(self.message)


class LoginServiceException(Exception):
    def __init__(self, message=Constant.LOGIN_UNEXPECTED_ERROR_MESSAGE):
        self.message = message
        super().__init__(self.message)
