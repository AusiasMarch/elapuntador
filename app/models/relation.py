from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

# from app.models.base import Base, BaseDB, BaseDBCreate, BaseDBUpdate
# from app.models.metric import FeatureImportanceOut, TestPredictionOut

class Relation(BaseModel):
    id: int
    relation: str

    def __repr__(self):
        return '<Relation(id={}, relation={})>'.format(self.id, self.relation)

    def __str__(self):
        return '<Relation(id={}, relation={})>'.format(self.id, self.relation)


class RelationInDb(Relation):
    pass
    

class RelationCreate(Relation):
    id: Optional[int]