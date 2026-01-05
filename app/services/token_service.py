# services/token_service.py
import secrets
from datetime import datetime, timedelta

def generate_verification_token():
    return secrets.token_urlsafe(32)

def token_expiry():
    return datetime.utcnow() + timedelta(minutes=15)


