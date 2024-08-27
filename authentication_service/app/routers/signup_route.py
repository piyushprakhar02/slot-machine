from fastapi import APIRouter, HTTPException, Depends
from app.database import Session

from app.schemas.signup_schema import UserSignupSchema, UserSignupVerificationSchema, UserSignupResponseSchema, UserSignupVerificationResponseSchema
from app.services.signup_service import UserSignupService, SignupServiceException, SignupUsernameExistsException, SignupVerificationException
from app.database import get_db
from constant import Constant

router = APIRouter()


@router.post("",
             summary="User Signup",
             description="Endpoint for user registration. Users provide their email, name, birthdate, and password to create a new account. If successful, an email is returned. If the email already exists, a 400 error is raised.",
             response_model=UserSignupResponseSchema,
             response_description="Successful signup response with the user's email.")
async def signup(data: UserSignupSchema, db: Session = Depends(get_db)):
    user_signup_service = UserSignupService(db)
    try:
        if user_signup_service.register(data):
            return {"success": True, "email": data.email}

    except SignupUsernameExistsException:
        raise HTTPException(status_code=400, detail=Constant.SIGNUP_USER_EXISTS_EXCEPTION_MESSAGE)

    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/verify",
             summary="User Signup Verification",
             description="Endpoint for verifying user registration. Users provide their email and verification code to verify their account. If successful, the user's email is returned.",
             response_model=UserSignupVerificationResponseSchema,
             response_description="Successful verification response with the user's email."
             )
async def verify(data: UserSignupVerificationSchema, db: Session = Depends(get_db)):
    user_signup_service = UserSignupService(db)
    try:
        if user_signup_service.verify(data):
            return {"success": True, "email": data.email}

    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
