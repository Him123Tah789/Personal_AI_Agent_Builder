from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_BASE_URL: str = "http://localhost:8000"
    WEB_BASE_URL: str = "http://localhost:3000"

    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/jarvis"
    JWT_SECRET: str = "change-me"
    JWT_ISSUER: str = "jarvis-api"
    JWT_AUDIENCE: str = "jarvis-web"

    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
    GOOGLE_REDIRECT_URI: str = "http://localhost:3000/callback"

    # Must be 32 bytes base64 url-safe
    TOKEN_ENC_KEY: str = "change-me-to-32-bytes-base64-url-safe-key-here"

    class Config:
        env_file = ".env"

settings = Settings()
