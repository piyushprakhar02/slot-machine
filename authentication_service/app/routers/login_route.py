from fastapi import APIRouter, HTTPException, Depends
from app.database import Session

from app.schemas.login_schema import UserLoginSchema, UserLoginResponseSchema, MFAChallengeRequestSchema, MFAChallengeResponseSchema
from app.services.login_service import UserLoginService, LoginServiceException, InvalidCredentialsException
from app.database import get_db
from constant import Constant

router = APIRouter()


@router.post("",
             summary="User Login",
             description="Endpoint for user login. Users can authenticate by providing their credentials. If MFA is required, the MFA challenge must be completed using the `/respond-to-challenge` endpoint.",
             response_description="Successful login response with a message.")
async def login(data: UserLoginSchema, db: Session = Depends(get_db)):
    user_login_service = UserLoginService(db)
    try:
        message = user_login_service.login(data)
        return {"success": True, "message": message}

    except LoginServiceException:
        raise HTTPException(status_code=400, detail=Constant.LOGIN_UNEXPECTED_ERROR_MESSAGE)

    except InvalidCredentialsException:
        raise HTTPException(status_code=400, detail=Constant.LOGIN_INVALID_CREDENTIALS_ERROR_MESSAGE)

    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/respond-to-challenge", summary="Complete MFA Challenge",
             description="Endpoint to respond to an MFA challenge. Users provide the email, session obtained from aws login api, and MFA code to complete the MFA process and receive an access token.",
             response_description="Successful MFA response with a message and access token.",
             response_model=MFAChallengeResponseSchema)
async def complete_mfa(data: MFAChallengeRequestSchema, db: Session = Depends(get_db)):
    user_login_service = UserLoginService(db=db)
    try:
        token = user_login_service.respond_to_mfa_challenge(email=data.email, session=data.session, code=data.code)
        return {"success": True, "message": "Challenge passed successfully", "access_token": token}

    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
