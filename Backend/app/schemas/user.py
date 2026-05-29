from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.user import UserRole


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    role: UserRole | None = None
    is_active: bool | None = None


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
