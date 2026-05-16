from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class ActivityLogEntry(BaseModel):
    action: str
    timestamp: datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    role: str = "user"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    role: str


class UserInDB(BaseModel):
    email: EmailStr
    hashed_password: str
    role: str = "user"
    activity_log: list[ActivityLogEntry] = []