import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship

from db.base_class import Base


class Peso(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    kilos = Column(Integer)
    gramos = Column(Integer)
    query_text = Column(Integer, String)
    datetime = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="pesos")
