from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base


class Reporter(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    relation_id = Column(int, ForeignKey="relation.id")
    
    pesos = relationship("Peso", back_populates="reporter")
    relation = relationship("Relation", back_populates="reporters")