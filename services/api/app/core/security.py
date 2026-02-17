from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings

def create_access_token(sub: str, org_id: str, minutes: int = 60*24*7):
    now = datetime.now(timezone.utc)
    payload = {
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "sub": sub,
        "org_id": org_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=minutes)).timestamp()),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
