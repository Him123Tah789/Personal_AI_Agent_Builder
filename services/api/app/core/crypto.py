import base64
from cryptography.fernet import Fernet
from app.core.config import settings

def _fernet() -> Fernet:
    # Ensure key is bytes
    key = settings.TOKEN_ENC_KEY
    if not key:
        raise ValueError("TOKEN_ENC_KEY is not set")
    return Fernet(key.encode())

def encrypt(text: str) -> str:
    return _fernet().encrypt(text.encode()).decode()

def decrypt(token_enc: str) -> str:
    return _fernet().decrypt(token_enc.encode()).decode()
