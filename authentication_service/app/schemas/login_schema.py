from pydantic import BaseModel, EmailStr, SecretStr


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: SecretStr


class UserLoginResponseSchema(BaseModel):
    success: bool
    token: str


class MFAChallengeRequestSchema(BaseModel):
    email: EmailStr
    session: str
    code: str


class MFAChallengeResponseSchema(BaseModel):
    success: bool
    access_token: str
    message: str
