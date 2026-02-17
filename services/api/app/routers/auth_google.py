from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import create_access_token
from app.core.crypto import encrypt
from app.db.session import get_db
from app.services.google_oauth import exchange_code_for_tokens, fetch_userinfo, expiry_from
# Import models to use them (mock for MVP)
# from app.db.models.user import User

router = APIRouter(prefix="/auth/google", tags=["auth"])

class GoogleCallbackIn(BaseModel):
    code: str
    code_verifier: str
    org_name: str | None = None

@router.post("/callback")
async def google_callback(payload: GoogleCallbackIn, db: Session = Depends(get_db)):
    # 1) Exchange code -> tokens
    try:
        # Check if secrets are set
        if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
             raise HTTPException(status_code=500, detail="Google Client credentials not configured.")

        token_data = await exchange_code_for_tokens(
            settings.GOOGLE_CLIENT_ID,
            settings.GOOGLE_CLIENT_SECRET,
            payload.code,
            settings.GOOGLE_REDIRECT_URI,
            payload.code_verifier,
        )
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to exchange code: {str(e)}")

    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    expires_in = token_data.get("expires_in")
    scope = token_data.get("scope", "")

    if not access_token:
        raise HTTPException(status_code=400, detail="No access_token returned")

    # 2) Userinfo
    try:
        userinfo = await fetch_userinfo(access_token)
    except Exception as e:
         raise HTTPException(status_code=400, detail="Failed to fetch userinfo")
         
    email = userinfo.get("email")
    sub = userinfo.get("sub")
    name = userinfo.get("name")
    picture = userinfo.get("picture")

    if not email or not sub:
        raise HTTPException(status_code=400, detail="Incomplete userinfo")

    # 3) MVP: Create Org/User if not exists (Simplified for Blueprint)
    # In a real implementation:
    # user = crud.get_user_by_email(db, email)
    # if not user: user = crud.create_user(...)
    
    # For now, we simulate success and return a JWT
    org_id = "00000000-0000-0000-0000-000000000000" # Placeholder UUID
    jwt_token = create_access_token(sub=email, org_id=org_id)

    # We would encrypt and store tokens here
    # enc_access = encrypt(access_token)
    
    return {
        "access_token": jwt_token,
        "user": {"email": email, "name": name, "picture": picture},
        "scopes": scope,
        "google_sub": sub,
        "expires_at": expiry_from(expires_in).isoformat() if expires_in else None,
    }
