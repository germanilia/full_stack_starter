from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    

class UserResponse(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)