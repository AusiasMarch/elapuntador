from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

# from app.models.base import Base, BaseDB, BaseDBCreate, BaseDBUpdate
# from app.models.metric import FeatureImportanceOut, TestPredictionOut

class Peso(BaseModel):
    id: int
    user_id: int
    kilos: int
    gramos: int

    def __repr__(self):
        return '<Peso(kilos={}, gramos={})>'.format(self.kilos, self.gramos)


class PesoInDb(Peso):
    datetime: datetime
    

class PesoCreate(Peso):
    id: Optional[int]
    gramos: Optional[int]
    kilos: Optional[int]
    gramos: Optional[int]