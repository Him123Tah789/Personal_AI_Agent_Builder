from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token
from app.core.crypto import encrypt
from app.core.deps import get_db
from app.services.google_oauth import exchange_code_for_tokens, fetch_userinfo, expiry_from
from app.db.models.user import User
from app.db.models.org import Org
from app.db.models.membership import Membership
from app.db.models.integration_google import GoogleIntegration
from app.db.models.audit_log import AuditLog

router = APIRouter(prefix="/auth/google", tags=["auth"])

class GoogleCallbackIn(BaseModel):
    code: str
    code_verifier: str
    org_name: str | None = None

@router.post("/callback")
async def google_callback(payload: GoogleCallbackIn, db: Session = Depends(get_db)):
    # 1) Exchange code -> tokens
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="Google Client credentials not configured.")

    try:
        token_data = await exchange_code_for_tokens(
            settings.GOOGLE_CLIENT_ID,
            settings.GOOGLE_CLIENT_SECRET,
            payload.code,
            settings.GOOGLE_REDIRECT_URI,
            payload.code_verifier,
        )
    except Exception as e:
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
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to fetch userinfo")

    email = userinfo.get("email")
    sub = userinfo.get("sub")
    name = userinfo.get("name")
    picture = userinfo.get("picture")

    if not email or not sub:
        raise HTTPException(status_code=400, detail="Incomplete userinfo")

    # 3) Upsert User + Org + Membership + GoogleIntegration
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, full_name=name, avatar_url=picture, last_login_at=datetime.now(timezone.utc))
        db.add(user)
        db.flush()
        org = Org(name=payload.org_name or "Founder Org")
        db.add(org)
        db.flush()
        db.add(Membership(org_id=org.id, user_id=user.id, role="OWNER"))
        org_id = org.id
    else:
        user.full_name = name
        user.avatar_url = picture
        user.last_login_at = datetime.now(timezone.utc)
        mem = db.query(Membership).filter(Membership.user_id == user.id).first()
        if not mem:
            org = Org(name=payload.org_name or "Founder Org")
            db.add(org)
            db.flush()
            db.add(Membership(org_id=org.id, user_id=user.id, role="OWNER"))
            org_id = org.id
        else:
            org_id = mem.org_id

    # 4) Upsert Google integration (encrypted tokens)
    integ = db.query(GoogleIntegration).filter(
        GoogleIntegration.org_id == org_id, GoogleIntegration.user_id == user.id
    ).first()
    if not integ:
        integ = GoogleIntegration(
            org_id=org_id,
            user_id=user.id,
            google_sub=sub,
            scopes=scope,
            access_token_enc=encrypt(access_token),
            refresh_token_enc=encrypt(refresh_token) if refresh_token else None,
            expiry=expiry_from(expires_in),
        )
        db.add(integ)
    else:
        integ.google_sub = sub
        integ.scopes = scope
        integ.access_token_enc = encrypt(access_token)
        if refresh_token:
            integ.refresh_token_enc = encrypt(refresh_token)
        integ.expiry = expiry_from(expires_in)

    # 5) Audit log
    db.add(AuditLog(org_id=org_id, user_id=user.id, action="AUTH_GOOGLE_CONNECTED", meta={"scopes": scope}))
    db.commit()

    # 6) Return JWT
    jwt_token = create_access_token(sub=email, org_id=str(org_id))
    return {
        "access_token": jwt_token,
        "user": {"email": email, "name": name, "picture": picture},
    }
