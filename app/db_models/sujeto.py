from sqlalchemy import DateTime, Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from db.base_class import Base


class Sujeto(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    apodos = Column(ARRAY(String))
    birth = Column(DateTime)

    pesos = relationship("Peso", back_populates="sujeto")
    alturas = relationship("Altura", back_populates="sujeto")
    tomas = relationship("Toma", back_populates="sujeto")
    temperaturas = relationship("Temperatura", back_populates="sujeto")