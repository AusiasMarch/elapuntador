from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from db_models.temperatura import Temperatura
from models.temperatura import TemperaturaCreate


def get_by_id(db_session: Session, *, temperatura_id: int) -> Optional[Temperatura]:
    return db_session.query(Temperatura).filter(Temperatura.id == temperatura_id).first()


def get_all(db_session: Session) -> List[Optional[Temperatura]]:
    return db_session.query(Temperatura).all()


def get_all_by_user(
    db_session: Session, *, user_id: int
) -> List[Optional[Temperatura]]:
    return (
        db_session.query(Temperatura)
        .filter(Temperatura.user_id == user_id)
        .all()
    )


def create(db_session: Session, *, temperatura_in: TemperaturaCreate) -> Temperatura:
    temperatura_in_data = jsonable_encoder(temperatura_in)
    temperatura = Temperatura(**temperatura_in_data)
    db_session.add(temperatura)
    db_session.commit()
    db_session.refresh(temperatura)
    
    return temperatura