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
    
class PesoCreate(Peso):
    id: Optional[int]
    gramos: Optional[int]