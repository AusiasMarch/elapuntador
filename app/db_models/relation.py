from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base


class Relation(Base):
    id = Column(Integer, primary_key=True, index=True)
    relation = Column(String, index=True)

    reporter = relationship("Reporter", back_populates="relation")