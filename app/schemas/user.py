from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    is_banned: bool

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)