from sqlalchemy import DateTime, Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from db.base_class import Base


class Sujeto(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    gender = Column(String)
    apodos = Column(ARRAY(String))
    birth = Column(DateTime)

    pesos = relationship("Peso", back_populates="sujeto")
    alturas = relationship("Altura", back_populates="sujeto")
    tomas = relationship("Toma", back_populates="sujeto")
    temperaturas = relationship("Temperatura", back_populates="sujeto")
    
    def __repr__(self):
        return f'<Sujeto(name={self.name})>'
    
    def __str__(self):
        return f'<Sujeto(name={self.name})>'