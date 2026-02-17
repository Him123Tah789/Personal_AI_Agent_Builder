import httpx
from datetime import datetime, timezone, timedelta

CAL_BASE = "https://www.googleapis.com/calendar/v3"

def _auth_headers(access_token: str):
    return {"Authorization": f"Bearer {access_token}"}

async def list_upcoming_events(access_token: str, days: int = 7, calendar_id: str = "primary", max_results: int = 20):
    now = datetime.now(timezone.utc)
    time_min = now.isoformat()
    time_max = (now + timedelta(days=days)).isoformat()

    params = {
        "timeMin": time_min,
        "timeMax": time_max,
        "singleEvents": "true",
        "orderBy": "startTime",
        "maxResults": max_results,
    }

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(f"{CAL_BASE}/calendars/{calendar_id}/events", headers=_auth_headers(access_token), params=params)
        r.raise_for_status()
        return r.json()
