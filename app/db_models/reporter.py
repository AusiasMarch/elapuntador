from sqlalchemy import ForeignKey, Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from db.base_class import Base


class Reporter(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    relation_id = Column(Integer, ForeignKey("relation.id"))
    
    pesos = relationship("Peso", back_populates="reporter")
    relation = relationship("Relation", back_populates="reporters")
