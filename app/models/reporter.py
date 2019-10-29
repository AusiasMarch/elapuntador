from pydantic import BaseModel
from typing import Optional


# Shared properties
class ReporterBase(BaseModel):
    email: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    full_name: Optional[str] = None
    relation: Optional[str] = None

    class Config:
        orm_mode = True


class ReporterBaseInDB(ReporterBase):
    id: int = None


# Properties to receive via API on creation
class ReporterCreate(ReporterBaseInDB):
    email: str
    password: str


# Properties to receive via API on update
class ReporterUpdate(ReporterBaseInDB):
    password: Optional[str] = None


# Additional properties to return via API
class Reporter(ReporterBaseInDB):
    pass


# Additional properties stored in DB
class ReporterInDB(ReporterBaseInDB):
    hashed_password: str
