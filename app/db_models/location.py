from sqlalchemy import Column, Integer, Float, String
from geoalchemy2 import Geometry

from db.base_class import Base


class Location(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    center = Column(Geometry(geometry_type='POINT', srid=4326))
    radius = Column(Float)

    def __repr__(self):
        return '<Location(name={})>'.format(self.name)

    def __str__(self):
        return '<Location(name={})>'.format(self.name)