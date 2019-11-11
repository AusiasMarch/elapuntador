import datetime
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship

from db.base_class import Base


class Peso_Girls_Who(Base):
    day = Column(Float, primary_key=True, index=True)
    L = Column(Integer)
    M = Column(Float)
    S = Column(Float)
    P01 = Column(Float)
    P1 = Column(Float)
    P3 = Column(Float)
    P5 = Column(Float)
    P10 = Column(Float)
    P15 = Column(Float)
    P25 = Column(Float)
    P50 = Column(Float)
    P75 = Column(Float)
    P85 = Column(Float)
    P90 = Column(Float)
    P95 = Column(Float)
    P97 = Column(Float)
    P99 = Column(Float)
    P999 = Column(Float)
    

class Peso_Boys_Who(Base):
    day = Column(Float, primary_key=True, index=True)
    L = Column(Integer)
    M = Column(Float)
    S = Column(Float)
    P01 = Column(Float)
    P1 = Column(Float)
    P3 = Column(Float)
    P5 = Column(Float)
    P10 = Column(Float)
    P15 = Column(Float)
    P25 = Column(Float)
    P50 = Column(Float)
    P75 = Column(Float)
    P85 = Column(Float)
    P90 = Column(Float)
    P95 = Column(Float)
    P97 = Column(Float)
    P99 = Column(Float)
    P999 = Column(Float)
