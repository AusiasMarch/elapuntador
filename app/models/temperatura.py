from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# from app.models.base import Base, BaseDB, BaseDBCreate, BaseDBUpdate
# from app.models.metric import FeatureImportanceOut, TestPredictionOut

class Temperatura(BaseModel):
    id: int
    sujeto_id: int
    user_id: int
    query_text: str
    ip: str
    grados: int

    def __repr__(self):
        return '<Temperatura(grados={})>'.format(self.grados)


class TemperaturaInDb(Temperatura):
    datetime: datetime
    

class TemperaturaCreate(Temperatura):
    id: Optional[int]