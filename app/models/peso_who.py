from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# from app.models.base import Base, BaseDB, BaseDBCreate, BaseDBUpdate
# from app.models.metric import FeatureImportanceOut, TestPredictionOut

class PesoWho(BaseModel):
    day: float
    L: int
    M: float
    S: float
    P01: float
    P1: float
    P3: float
    P5: float
    P10: float
    P15: float
    P25: float
    P50: float
    P75: float
    P85: float
    P90: float
    P95: float
    P97: float
    P99: float
    P999: float


