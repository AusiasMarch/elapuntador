import datetime

from pydantic import BaseModel
from typing import Optional, List


# Shared properties
class SujetoBase(BaseModel):
    id: int
    name: str
    gender: str
    apodos: Optional[List[str]]
    birth: datetime.datetime
    
    def __repr__(self):
        return f'<Sujeto(name={self.name})>'
    
    def __str__(self):
        return f'<Sujeto(name={self.name})>'


class SujetoCreate(SujetoBase):
    id:  Optional[int] = None

