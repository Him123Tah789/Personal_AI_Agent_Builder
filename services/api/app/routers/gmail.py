from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.services.token_store import get_valid_google_access_token
from app.services.gmail_service import list_threads, get_thread, create_draft
from app.db.models.audit_log import AuditLog

router = APIRouter(prefix="/gmail", tags=["gmail"])

@router.get("/threads")
async def gmail_threads(max: int = 10, q: str | None = None, ctx=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        token = await get_valid_google_access_token(db, ctx["org_id"], ctx["user"].id)
        data = await list_threads(token, max_results=max, q=q)
        db.add(AuditLog(org_id=ctx["org_id"], user_id=ctx["user"].id, action="GMAIL_LIST_THREADS", meta={"max": max, "q": q}))
        db.commit()
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/thread/{thread_id}")
async def gmail_thread(thread_id: str, ctx=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        token = await get_valid_google_access_token(db, ctx["org_id"], ctx["user"].id)
        data = await get_thread(token, thread_id)
        db.add(AuditLog(org_id=ctx["org_id"], user_id=ctx["user"].id, action="GMAIL_GET_THREAD", resource_type="thread", resource_id=thread_id))
        db.commit()
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/draft")
async def gmail_draft(payload: dict, ctx=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        token = await get_valid_google_access_token(db, ctx["org_id"], ctx["user"].id)
        data = await create_draft(token, payload["to"], payload["subject"], payload["body"])
        db.add(AuditLog(org_id=ctx["org_id"], user_id=ctx["user"].id, action="GMAIL_CREATE_DRAFT", meta={"to": payload["to"]}))
        db.commit()
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
