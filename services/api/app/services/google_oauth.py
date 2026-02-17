import httpx
from datetime import datetime, timezone, timedelta

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

async def exchange_code_for_tokens(client_id: str, client_secret: str, code: str, redirect_uri: str, code_verifier: str):
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier,
    }
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(GOOGLE_TOKEN_URL, data=data)
        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            # Add logging here in real app
            print(f"Token Exchange Failed: {r.text}")
            raise e
        return r.json()

async def fetch_userinfo(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(GOOGLE_USERINFO_URL, headers=headers)
        r.raise_for_status()
        return r.json()

def expiry_from(expires_in: int | None):
    if not expires_in:
        return None
    return datetime.now(timezone.utc) + timedelta(seconds=int(expires_in))
