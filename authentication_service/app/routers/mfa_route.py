from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database import get_db
from app.services.mfa_service import MFAService
from app.schemas.mfa_schema import MFAEnableRequestSchema, MFASetupRequestSchema, MFASetupResponseSchema, MFAInitializeResponseSchema, MFAEnableResponseSchema

router = APIRouter()

bearer_scheme = HTTPBearer()


@router.post("/initiate", response_model=MFAInitializeResponseSchema,
             summary="Initiate MFA Setup",
             description="Initiates the setup process for Multi-Factor Authentication (MFA). Returns a setup code that users should configure in their authenticator app.",
             response_description="Successful response with a setup code for MFA initiation."
             )
async def setup_mfa(db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    mfa_service = MFAService(access_token=token, db=db)
    try:
        setup_code = mfa_service.initiate_mfa_setup()
        return {"success": True, "message": "MFA setup initiated. Please configure your authenticator app.", "code": setup_code}

    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/setup", response_model=MFASetupResponseSchema,
             summary="Complete MFA Setup",
             description="Finalizes the Multi-Factor Authentication (MFA) setup by verifying the Time-based One-Time Password (TOTP) provided by the user. This endpoint should be used after the user has configured their authenticator app and obtained a TOTP.",
             response_description="Successful response indicating MFA setup completion."
             )
async def complete_mfa(data: MFASetupRequestSchema, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    mfa_service = MFAService(access_token=token, db=db)
    try:
        if mfa_service.complete_mfa_setup(setup_code=data.code):
            return {"success": True, "message": "MFA setup completed successfully"}
        else:
            raise HTTPException(status_code=400, detail="Invalid setup code")

    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/enable", response_model=MFAEnableResponseSchema,
             summary="Enable MFA",
             description="Enables MFA for a user account. This endpoint should be used after completing MFA setup.",
             response_description="Successful response indicating MFA was enabled successfully."
             )
async def complete_mfa(data: MFAEnableRequestSchema, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    mfa_service = MFAService(access_token=token, db=db)
    try:
        if mfa_service.enable_totp_mfa(data.email):
            return {"success": True, "message": "MFA enabled successfully"}
        else:
            raise HTTPException(status_code=400, detail="Invalid setup code")

    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
