from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base


class Relation(Base):
    id = Column(Integer, primary_key=True, index=True)
    relation = Column(String, index=True)

    # user = relationship("User", back_populates="relation_id")