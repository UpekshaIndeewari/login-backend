# schemas/user.py
from pydantic import BaseModel, EmailStr

class RegisterUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    confirm_password: str

class LoginUser(BaseModel):
    email: EmailStr
    password: str
