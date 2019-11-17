from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    can_report = Column(Boolean(), default=False)
    relation_id = Column(Integer, ForeignKey("relation.id"))

    pesos = relationship("Peso", back_populates="user")
    alturas = relationship("Altura", back_populates="user")
    tomas = relationship("Toma", back_populates="user")
    temperaturas = relationship("Temperatura", back_populates="user")
    # relation = relationship("Relation")

    def __repr__(self):
        return f'<User(full_name={self.full_name}, relation={self.relation.relation})>'

    def __str__(self):
        return f'<User(full_name={self.full_name}, relation={self.relation.relation})>'