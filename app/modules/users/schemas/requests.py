from pydantic import BaseModel, EmailStr
from app.modules.users.models.user import UserRole

class UserCreateRequest(BaseModel):
    name: str
    email: EmailStr
    role: UserRole

class UserUpdateRequest(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    role: UserRole | None = None
