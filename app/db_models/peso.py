from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Peso(Base):
    id = Column(Integer, primary_key=True, index=True)
    reporter_id = Column(Integer, ForeignKey("reporter.id"))
    kilos = Column(Integer)
    gramos = Column(Integer)
    datetime = Column(DateTime)