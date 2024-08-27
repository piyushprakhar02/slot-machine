from decouple import config
from utils.cognito_utils import get_cognito_client
from app.database import Session
from constant import Constant
from app.services.sns_service import SnsService
from app.repositories.user_repository import UserRepository
from datetime import datetime
from app.schemas.signup_schema import UserSignupSchema, UserSignupVerificationSchema

CLIENT_ID = config('AWS_COGNITO_CLIENT_ID')


class UserSignupService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, data: UserSignupSchema) -> bool:
        cognito_client = get_cognito_client()
        try:
            response = cognito_client.sign_up(
                ClientId=CLIENT_ID,
                Username=data.email,
                Password=data.password.get_secret_value(),
                UserAttributes=[
                    {'Name': 'email', 'Value': data.email},
                    {'Name': 'name', 'Value': data.name},
                    {'Name': 'birthdate', 'Value': datetime.strftime(data.birthdate, "%Y-%m-%d")},
                ]
            )

            user_cognito_id = response['UserSub']

            # Create the user in the database
            user_service = UserRepository(db=self.db)
            user_service.add_user(id=user_cognito_id, email=data.email, name=data.name, birthdate=datetime.strftime(data.birthdate, "%Y-%m-%d"))

            return True

        except cognito_client.exceptions.UsernameExistsException:
            self.db.rollback()
            raise SignupUsernameExistsException()

        except Exception as e:
            self.db.rollback()
            print(f"Exception: {e}")
            raise SignupServiceException()

    def verify(self, data: UserSignupVerificationSchema):
        totp = data.totp
        email = data.email
        cognito_client = get_cognito_client()
        response = cognito_client.confirm_sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            ConfirmationCode=totp
        )

        # Credit tokens for successful signup
        message_body = {
            "user_id": email,
            "operation": Constant.CREDIT_TOKEN,
            "amount": Constant.NUMBER_OF_TOKENS_ON_SIGNUP
        }

        sns_service = SnsService()
        sns_service.publish(message_body=message_body)

        return True


class SignupServiceException(Exception):
    def __init__(self, message=Constant.SIGNUP_UNEXPECTED_ERROR_MESSAGE):
        self.message = message
        super().__init__(self.message)


class SignupUsernameExistsException(Exception):
    def __init__(self, message=Constant.SIGNUP_USER_EXISTS_EXCEPTION_MESSAGE):
        self.message = message
        super().__init__(self.message)


class SignupVerificationException(Exception):
    def __init__(self, message=Constant.SIGNUP_VERIFICATION_UNEXPECTED_ERROR_MESSAGE):
        self.message = message
        super().__init__(self.message)
