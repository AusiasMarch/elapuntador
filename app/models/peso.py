from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

# from app.models.base import Base, BaseDB, BaseDBCreate, BaseDBUpdate
# from app.models.metric import FeatureImportanceOut, TestPredictionOut

class Peso(BaseModel):
    id: int
    reporter_id: int
    kilos: int
    gramos: int

    def __repr__(self):
        return '{} kilos {} gramos'.format(self.kilos, self.gramos)
    
class PesoCreate(Peso):
    id: Optional[int]
    gramos: Optional[int]