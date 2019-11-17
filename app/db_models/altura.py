import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship

from db.base_class import Base


class Altura(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    sujeto_id = Column(Integer, ForeignKey("sujeto.id"))
    centimetros = Column(Integer)
    query_text = Column(String)
    datetime = Column(DateTime, default=datetime.datetime.utcnow)
    ip = Column(String)

    user = relationship("User", back_populates="alturas")
    sujeto = relationship("Sujeto", back_populates="alturas")

    def __repr__(self):
        return '<Altura(centimetros={})>'.format(self.kilos, self.gramos)

    def __str__(self):
        return '<Altura(centimetros={})>'.format(self.kilos, self.gramos)
