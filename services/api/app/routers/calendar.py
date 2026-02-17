from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.services.token_store import get_valid_google_access_token
from app.services.calendar_service import list_upcoming_events
from app.db.models.audit_log import AuditLog

router = APIRouter(prefix="/calendar", tags=["calendar"])

@router.get("/upcoming")
async def upcoming(days: int = 7, ctx=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        token = await get_valid_google_access_token(db, ctx["org_id"], ctx["user"].id)
        data = await list_upcoming_events(token, days=days)
        db.add(AuditLog(org_id=ctx["org_id"], user_id=ctx["user"].id, action="CAL_LIST_UPCOMING", meta={"days": days}))
        db.commit()
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
