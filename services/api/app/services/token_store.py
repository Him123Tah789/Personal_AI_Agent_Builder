from datetime import datetime, timezone, timedelta
import httpx
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.crypto import decrypt, encrypt
from app.db.models.integration_google import GoogleIntegration

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

def _is_expired(expiry):
    if not expiry:
        return True
    # refresh a bit early
    return datetime.now(timezone.utc) >= (expiry - timedelta(seconds=60))

async def get_valid_google_access_token(db: Session, org_id: str, user_id):
    integ = (
        db.query(GoogleIntegration)
        .filter(GoogleIntegration.org_id == org_id, GoogleIntegration.user_id == user_id)
        .first()
    )
    if not integ:
        raise ValueError("Google integration not found")

    access_token = decrypt(integ.access_token_enc)

    if not _is_expired(integ.expiry):
        return access_token

    if not integ.refresh_token_enc:
        raise ValueError("Missing refresh token. Reconnect Google with consent.")

    refresh_token = decrypt(integ.refresh_token_enc)

    data = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(GOOGLE_TOKEN_URL, data=data)
        r.raise_for_status()
        td = r.json()

    new_access = td.get("access_token")
    expires_in = td.get("expires_in")

    if not new_access:
        raise ValueError("Refresh failed: no access_token")

    integ.access_token_enc = encrypt(new_access)
    if expires_in:
        integ.expiry = datetime.now(timezone.utc) + timedelta(seconds=int(expires_in))
    db.add(integ)
    db.commit()

    return new_access
