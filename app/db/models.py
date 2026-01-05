# db/models.py
from sqlalchemy import Column, Integer, String, TIMESTAMP,Boolean
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashedpassword = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(255))
    token_expires_at = Column(TIMESTAMP)
    reset_token = Column(String(255), nullable=True)
    reset_token_expires_at = Column(TIMESTAMP, nullable=True)
    
