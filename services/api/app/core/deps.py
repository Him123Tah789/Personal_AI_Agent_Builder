from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.db.models.user import User
from app.db.models.membership import Membership

bearer = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
):
    token = creds.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"], audience=settings.JWT_AUDIENCE)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    email = payload.get("sub")
    org_id = payload.get("org_id")
    if not email or not org_id:
        raise HTTPException(status_code=401, detail="Invalid token claims")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    membership = db.query(Membership).filter(Membership.org_id == org_id, Membership.user_id == user.id).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Not a member of org")

    return {"user": user, "org_id": org_id, "role": membership.role}
