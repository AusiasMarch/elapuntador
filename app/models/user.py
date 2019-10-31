from pydantic import BaseModel
from typing import Optional


# Shared properties
class UserBase(BaseModel):
    email: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    can_report: Optional[bool] = False
    full_name: Optional[str] = None
    relation_id: Optional[int] = None

    class Config:
        orm_mode = True


class UserBaseInDB(UserBase):
    id: int = None


# Properties to receive via API on creation
class UserCreate(UserBaseInDB):
    email: str
    password: str
    full_name: str
    relation: str


# Properties to receive via API on update
class UserUpdate(UserBaseInDB):
    password: Optional[str] = None


# Additional properties to return via API
class User(UserBaseInDB):
    pass


# Additional properties stored in DB
class UserInDB(UserBaseInDB):
    hashed_password: str
