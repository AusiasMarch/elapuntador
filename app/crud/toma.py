from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from db_models.toma import Toma
from models.toma import TomaCreate


def get_by_id(db_session: Session, *, toma_id: int) -> Optional[Toma]:
    return db_session.query(Toma).filter(Toma.id == toma_id).first()


def get_all(db_session: Session) -> List[Optional[Toma]]:
    return db_session.query(Toma).all()


def get_all_by_user(
    db_session: Session, *, user_id: int
) -> List[Optional[Toma]]:
    return (
        db_session.query(Toma)
        .filter(Toma.user_id == user_id)
        .all()
    )


def get_all_by_sujeto(
    db_session: Session, *, sujeto_id: int
) -> List[Optional[Toma]]:
    return (
        db_session.query(Toma)
        .filter(Toma.sujeto_id == sujeto_id)
        .all()
    )


def get_all_by_user_and_sujeto(
    db_session: Session, *, user_id: int, sujeto_id: int
) -> List[Optional[Toma]]:
    return (
        db_session.query(Toma)
        .filter(Toma.user_id == user_id)
        .filter(Toma.sujeto_id == sujeto_id)
        .all()
    )


def create(db_session: Session, *, toma_in: TomaCreate) -> Toma:
    toma_in_data = jsonable_encoder(toma_in)
    toma = Toma(**toma_in_data)
    db_session.add(toma)
    db_session.commit()
    db_session.refresh(toma)
    
    return toma