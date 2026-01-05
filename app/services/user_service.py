# service/user_service.py
from app.db.models import User
from app.core.security import hash_password

def create_user(db, user_data, token, expires_at):
    user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        hashedpassword=hash_password(user_data.password),
        is_verified=False,
        verification_token=token,
        token_expires_at=expires_at
    )
    db.add(user)
    db.commit()
    return user
