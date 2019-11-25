from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


class Users(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True, unique=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    can_report = Column(Boolean(), default=False)
    relation_id = Column(Integer, ForeignKey("relation.id"))

    alturas = relationship("Altura", back_populates="user")
    pesos = relationship("Peso", back_populates="user")
    relation = relationship("Relation", foreign_keys=relation_id)
    tomas = relationship("Toma", back_populates="user")
    temperaturas = relationship("Temperatura", back_populates="user")

    def __repr__(self):
        return f'<User(full_name={self.full_name})>'

    def __str__(self):
        return f'<User(full_name={self.full_name})>'