class Constant:
    CREDIT_TOKEN = "CREDIT"
    DEBIT_TOKEN = "DEBIT"

    NUMBER_OF_TOKENS_ON_SIGNUP = 10
    NUMBER_OF_TOKENS_ON_LOGIN = 1

    LOGIN_INVALID_CREDENTIALS_ERROR_MESSAGE = "The credentials you entered are not correct"
    LOGIN_UNEXPECTED_ERROR_MESSAGE = "An unexpected error occured"

    SIGNUP_USER_EXISTS_EXCEPTION_MESSAGE = "Email already exists"
    SIGNUP_UNEXPECTED_ERROR_MESSAGE = "An unexpected error occured"

    SIGNUP_VERIFICATION_UNEXPECTED_ERROR_MESSAGE = "An unexpected error occured"

    MFA_SETUP_WRONG_TOTP_EXCEPTION = "The provided TOTP code is incorrect."
    MFA_INITIATE_UNEXPECTED_ERROR_MESSAGE = "An unexpected error occured"
    MFA_SETUP_UNEXPECTED_ERROR_MESSAGE = "An unexpected error occured"
