from pydantic import BaseModel, BaseConfig
from geoalchemy2 import WKTElement
from typing import Optional

from models import coordinates

class LocationBase(BaseModel):
    id: int
    name: str


class Location(LocationBase):
    id: Optional[int]
    buffer: WKTElement
    
    def __repr__(self):
        return '<Location(name={})>'.format(self.name)

    def __str__(self):
        return '<Location(name={})>'.format(self.name)

    class Config(BaseConfig):
        arbitrary_types_allowed = True


class LocationCreate(LocationBase):
    id: Optional[int]
    center: coordinates.Coordinates
    radius: float
    
    def __repr__(self):
        return '<Location(name={})>'.format(self.name)

    def __str__(self):
        return '<Location(name={})>'.format(self.name)

    class Config(BaseConfig):
        arbitrary_types_allowed = True


class LocationInDb(LocationBase):
    id: Optional[int]
    buffer: WKTElement

    def __repr__(self):
        return '<Location(name={})>'.format(self.name)

    def __str__(self):
        return '<Location(name={})>'.format(self.name)

    class Config(BaseConfig):
        arbitrary_types_allowed = True

