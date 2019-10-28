from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db.base_class import Base


class Peso(Base):
    id = Column(Integer, primary_key=True, index=True)
    reporter = relationship("reporter", back_populates="reporter")
    kilos = Column(Integer)
    gramos = Column(Integer)
    datetime = Column(DateTime)