import datetime

from pydantic import BaseModel, BaseConfig
from typing import Optional, List
from geoalchemy2 import WKTElement

from models import coordinates


# Shared properties
class SujetoBase(BaseModel):
    id: int
    name: str
    gender: str = None
    apodos: Optional[List[str]]
    birth: datetime.datetime = None
    latlng: coordinates.Coordinates = None
    latlng_update: datetime.datetime = None
    latlng_car: bool = None
    
    def __repr__(self):
        return f'<Sujeto(name={self.name})>'
    
    def __str__(self):
        return f'<Sujeto(name={self.name})>'


class SujetoInDB(SujetoBase):
    coordiantes: WKTElement

    class Config(BaseConfig):
        arbitrary_types_allowed = True


class SujetoCreate(SujetoBase):
    id:  Optional[int] = None

