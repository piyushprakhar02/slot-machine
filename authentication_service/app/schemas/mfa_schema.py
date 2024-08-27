from pydantic import BaseModel, EmailStr, SecretStr


class MFAInitializeRequestSchema(BaseModel):
    email: EmailStr


class MFAInitializeResponseSchema(BaseModel):
    success: bool
    message: str
    code: str


class MFASetupRequestSchema(BaseModel):
    code: str


class MFASetupResponseSchema(BaseModel):
    success: bool
    message: str


class MFAEnableRequestSchema(BaseModel):
    email: str


class MFAEnableResponseSchema(BaseModel):
    success: bool
    message: str
