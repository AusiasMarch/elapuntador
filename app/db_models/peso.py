import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship

from db.base_class import Base


class Peso(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    sujeto_id = Column(Integer, ForeignKey("sujeto.id"))
    kilos = Column(Integer)
    gramos = Column(Integer)
    query_text = Column(String)
    datetime = Column(DateTime, default=datetime.datetime.utcnow)
    ip = Column(String)

    user = relationship("Users", foreign_keys=user_id, back_populates="pesos")
    sujeto = relationship("Sujeto", foreign_keys=sujeto_id, back_populates="pesos")

    def __repr__(self):
        return '<Peso(kilos={}, gramos={})>'.format(self.kilos, self.gramos)
    
    def __str__(self):
        return '<Peso(kilos={}, gramos={})>'.format(self.kilos, self.gramos)
