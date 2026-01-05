# routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.user import RegisterUser
from app.db.database import SessionLocal
from app.db.models import User
from app.services.user_service import create_user
from app.services.token_service import generate_verification_token, token_expiry
from app.services.email_service import send_verification_email
from datetime import datetime
from fastapi.responses import RedirectResponse
from app.schemas.user import LoginUser  # schema with email & password
from app.utils.hashing import verify_password  # function to compare hashed passwords
# from app.core.keycloak import get_current_user



router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: RegisterUser, db: Session = Depends(get_db)):

    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    try:
        # generate verification token
        token = generate_verification_token()
        expires_at = token_expiry()

        # create user with token
        create_user(db, user, token=token, expires_at=expires_at)

        # send verification email
        send_verification_email(user.email, token)

        return {
            "message": "Verification link has been sent to your email. Please verify before logging in."
        }

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    """
    Verifies user's email and redirects to login page.
    Handles expired links by redirecting to a "link expired" page.
    """
    # 1️⃣ Find user by token
    user = db.query(User).filter(User.verification_token == token).first()

    if not user:
        # Token invalid or already used
        raise HTTPException(status_code=400, detail="Invalid verification link")

    # 2️⃣ Check if token is expired
    if user.token_expires_at < datetime.utcnow():
        # Redirect to link expired page
        return RedirectResponse(url="http://localhost:5174/link-expired")

    # 3️⃣ Token valid → verify user
    user.is_verified = True
    user.verification_token = None
    user.token_expires_at = None

    # 4️⃣ Commit changes to DB BEFORE redirecting
    db.commit()
    db.refresh(user)  # optional, ensures the user object is updated

    # 5️⃣ Redirect to login page
    return RedirectResponse(url="http://localhost:5174/login")

@router.post("/login")
def login(user: LoginUser, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not db_user.is_verified:
        raise HTTPException(status_code=400, detail="Email is not verified")

    if not verify_password(user.password, db_user.hashedpassword):  # <-- fix here
        raise HTTPException(status_code=400, detail="Invalid email or password")

    db.commit()

    return {
        "success": True,
        "message": "Login successful",
        "first_name": db_user.first_name
    }

@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Email not found")

    # Generate reset token
    from app.services.reset_service import generate_reset_token, reset_token_expiry
    from app.services.email_service import send_reset_email

    token = generate_reset_token()
    expires_at = reset_token_expiry()

    user.reset_token = token
    user.reset_token_expires_at = expires_at
    db.commit()

    send_reset_email(user.email, token)
    return {"message": "Password reset link sent to your email."}

@router.post("/reset-password")
def reset_password(token: str = Query(...), new_password: str = Query(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.reset_token == token).first()
    if not user or not user.reset_token_expires_at or user.reset_token_expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired reset link")

    from app.core.security import hash_password
    user.hashedpassword = hash_password(new_password)

    # Clear reset token
    user.reset_token = None
    user.reset_token_expires_at = None

    db.commit()
    return {"message": "Password has been reset successfully"}


