# core/security.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # bcrypt limit: 72 bytes
    safe_password = password[:72]
    return pwd_context.hash(safe_password)
