from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from db_models.relation import Relation
from models.relation import RelationCreate


def get_by_id(db_session: Session, *, relation_id: int) -> Optional[Relation]:
    return db_session.query(Relation).filter(Relation.id == relation_id).first()


def get_by_relation(db_session: Session, *, relation: str) -> Optional[Relation]:
    return db_session.query(Relation).filter(Relation.relation == relation).first()


def get_all(db_session: Session) -> List[Optional[Relation]]:
    return db_session.query(Relation).all()


def get_all_by_user(
    db_session: Session, *, user_id: int
) -> List[Optional[Relation]]:
    return (
        db_session.query(Relation)
        .filter(Relation.user_id == user_id)
        .all()
    )


def create(db_session: Session, *, relation_in: RelationCreate) -> Relation:
    relation_in_data = jsonable_encoder(relation_in)
    relation = Relation(**relation_in_data)
    db_session.add(relation)
    db_session.commit()
    db_session.refresh(relation)
    
    print(relation)
    return relation