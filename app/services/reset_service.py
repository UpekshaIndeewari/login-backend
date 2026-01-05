# services/reset_service.py
import secrets
from datetime import datetime, timedelta

def generate_reset_token():
    return secrets.token_urlsafe(32)

def reset_token_expiry():
    return datetime.utcnow() + timedelta(minutes=15)
