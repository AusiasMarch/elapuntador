from typing import Optional
from models.base import Base


class ModelInfoBase(Base):
    fit_id: Optional[int]
    model_name: Optional[str]
    mse: Optional[float]


class ModelInfoDBCreate(ModelInfoBase):
    fit_id: int
    model: Optional[bytes]


class ModelInfoDBUpdate(ModelInfoBase):
    model: Optional[bytes]


class ModelInfoDB(ModelInfoBase):
    id: int
