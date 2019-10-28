from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.db_models.peso import Peso
from app.models.peso import PesoCreate


def get(db_session: Session, *, peso_id: int) -> Optional[Peso]:
    return db_session.query(Peso).filter(Peso.id == peso_id).first()


def get_all(db_session: Session, *) -> List[Optional[Peso]]:
    return db_session.query(Peso).all()


def get_all_by_reporter(
    db_session: Session, *, reporter_id: int
) -> List[Optional[Peso]]:
    return (
        db_session.query(Peso)
        .filter(Peso.reporter_id == reporter_id)
        .all()
    )


def insert_peso(db_session: Session, *, peso_in: PesoCreate) -> Peso:
    peso_in_data = jsonable_encoder(peso_in)
    peso = Peso(**peso_in_data)
    db_session.add(peso)
    db_session.commit()
    db_session.refresh(peso)
    
    return peso