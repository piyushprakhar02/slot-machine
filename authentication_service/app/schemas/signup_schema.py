from pydantic import BaseModel, EmailStr, SecretStr
from datetime import date


class UserSignupSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    name: str
    birthdate: date


class UserSignupVerificationSchema(BaseModel):
    email: EmailStr
    totp: str


class UserSignupResponseSchema(BaseModel):
    success: bool
    email: EmailStr


class UserSignupVerificationResponseSchema(BaseModel):
    success: bool
    email: EmailStr
