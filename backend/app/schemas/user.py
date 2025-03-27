from pydantic import BaseModel
from typing import List, Optional


class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    

class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True