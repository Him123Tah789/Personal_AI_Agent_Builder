from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth_google
# Import other routers as they are rebuilt (commenting out explicitly)
# from app.api.v1 import memory

app = FastAPI(title="Jarvis MVP API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.WEB_BASE_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_google.router)
# app.include_router(memory.router, prefix="/api/v1/memory", tags=["memory"])

@app.get("/health")
def health():
    return {"ok": True}
