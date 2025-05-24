from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.modules.users.models.user import UserRole

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
