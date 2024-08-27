from decouple import config
from utils.cognito_utils import get_cognito_client
from app.database import Session
from constant import Constant
from utils.cognito_utils import get_cognito_client_id

CLIENT_ID = config('AWS_COGNITO_CLIENT_ID')


class MFAService:
    def __init__(self, access_token: str, db: Session):
        self.db = db
        self.cognito_client = get_cognito_client()
        self.access_token = access_token

    def initiate_mfa_setup(self) -> str:
        cognito_client = get_cognito_client()
        try:
            response = cognito_client.associate_software_token(
                AccessToken=self.access_token
            )
            return response['SecretCode']
        except Exception as e:
            print(e)
            raise MFAInitiateException()

    def complete_mfa_setup(self, setup_code: str) -> bool:
        cognito_client = get_cognito_client()
        try:
            response = cognito_client.verify_software_token(
                UserCode=setup_code,
                AccessToken=self.access_token,
                FriendlyDeviceName="Device"
            )
            return response['Status'] == 'SUCCESS'

        except Exception as e:
            print(e)

    def enable_totp_mfa(self, email):
        try:
            response = self.cognito_client.set_user_mfa_preference(
                SoftwareTokenMfaSettings={
                    'Enabled': True,
                    'PreferredMfa': True
                },
                AccessToken=self.access_token
            )
            return True
        except self.cognito_client.exceptions.ClientError as e:
            print(f"An error occurred: {e}")
            raise

class MFASetupWrongOTPException(Exception):
    def __init__(self, message=Constant.MFA_SETUP_WRONG_TOTP_EXCEPTION):
        self.message = message
        super().__init__(self.message)


class MFAInitiateException(Exception):
    def __init__(self, message=Constant.MFA_INITIATE_UNEXPECTED_ERROR_MESSAGE):
        self.message = message
        super().__init__(self.message)


class MFASetupException(Exception):
    def __init__(self, message=Constant.MFA_SETUP_UNEXPECTED_ERROR_MESSAGE):
        self.message = message
        super().__init__(self.message)
