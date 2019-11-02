from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# from app.models.base import Base, BaseDB, BaseDBCreate, BaseDBUpdate
# from app.models.metric import FeatureImportanceOut, TestPredictionOut

class Toma(BaseModel):
    id: int
    user_id: int
    query_text: str
    ip: str
    centimetros: int

    def __repr__(self):
        return '<Peso(kilos={}, gramos={})>'.format(self.kilos, self.gramos)


class TomaInDb(Toma):
    datetime: datetime
    

class TomaCreate(Toma):
    id: Optional[int]