from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.models.user import UserRole


class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    role: UserRole
    cognito_sub: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)