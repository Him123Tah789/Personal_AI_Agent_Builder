from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic (e.g. connect to DB)
    print("Starting up Personal Founder AI Assistant Backend...")
    yield
    # Shutdown logic
    print("Shutting down...")

app = FastAPI(title="Personal Founder AI Assistant", lifespan=lifespan)

from app.auth import google
app.include_router(google.router, tags=["auth"])

from app.api.v1 import memory
app.include_router(memory.router, prefix="/api/v1/memory", tags=["memory"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Personal Founder AI Assistant API"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
