from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    google_id: str
    full_name: Optional[str] = None

class UserLogin(UserBase):
    password: str

class PasswordSet(BaseModel):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    email: str
    has_password: bool

class GoogleLogin(BaseModel):
    token: str # Google ID Token
