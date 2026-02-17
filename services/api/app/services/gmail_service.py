import base64
import httpx

GMAIL_BASE = "https://gmail.googleapis.com/gmail/v1/users/me"

def _auth_headers(access_token: str):
    return {"Authorization": f"Bearer {access_token}"}

async def list_threads(access_token: str, max_results: int = 10, q: str | None = None):
    params = {"maxResults": max_results}
    if q:
        params["q"] = q
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(f"{GMAIL_BASE}/threads", headers=_auth_headers(access_token), params=params)
        r.raise_for_status()
        return r.json()

async def get_thread(access_token: str, thread_id: str):
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(f"{GMAIL_BASE}/threads/{thread_id}", headers=_auth_headers(access_token))
        r.raise_for_status()
        return r.json()

def _make_rfc822(to_email: str, subject: str, body: str) -> str:
    msg = f"To: {to_email}\r\nSubject: {subject}\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n{body}"
    return msg

async def create_draft(access_token: str, to_email: str, subject: str, body: str):
    raw = _make_rfc822(to_email, subject, body)
    raw_b64 = base64.urlsafe_b64encode(raw.encode("utf-8")).decode("utf-8")

    payload = {"message": {"raw": raw_b64}}

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(f"{GMAIL_BASE}/drafts", headers=_auth_headers(access_token), json=payload)
        r.raise_for_status()
        return r.json()
