import datetime

from pydantic import BaseModel
from typing import Optional, List


# Shared properties
class SujetoBase(BaseModel):
    id: int
    name: str
    apodos: Optional[List[str]]
    birth: datetime.datetime


class SujetoCreate(SujetoBase):
    id:  Optional[int] = None

