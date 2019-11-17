from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base


class Relation(Base):
    id = Column(Integer, primary_key=True, index=True)
    relation = Column(String, index=True)

    def __repr__(self):
        return '<Relation(id={}, relation={})>'.format(self.id, self.relation)

    def __str__(self):
        return '<Relation(id={}, relation={})>'.format(self.id, self.relation)


    # user = relationship("User", back_populates="relation_id")