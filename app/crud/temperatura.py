import logging

import pandas as pd

from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from db_models.temperatura import Temperatura
from models.temperatura import TemperaturaCreate


log = logging.getLogger("elapuntador")


def get_by_id(db_session: Session, *, temperatura_id: int) -> Optional[Temperatura]:
    temperatura = db_session.query(
        Temperatura
    ).filter(
        Temperatura.id == temperatura_id
    ).first()
    log.debug(f"Temperatura got by id: {temperatura}")
    return temperatura


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


def get_all_by_sujeto(
    db_session: Session, *, sujeto_id: int
) -> List[Optional[Temperatura]]:
    temperatura_list = db_session.query(
        Temperatura
    ).filter(
        Temperatura.sujeto_id == sujeto_id
    ).all()
    
    temperaturas = pd.DataFrame(
        [(x.datetime, x.grados, x.decimas, x.ip, x.user_id, x.user.full_name) for x in
         temperatura_list],
        columns=['datetime', 'grados', 'decimas', 'ip', 'user_id', 'user_name'],
        index=[(x.id) for x in temperatura_list]
    )
    
    return temperaturas


def get_all_by_user_and_sujeto(
    db_session: Session, *, user_id: int, sujeto_id: int
) -> List[Optional[Temperatura]]:
    return (
        db_session.query(Temperatura)
        .filter(Temperatura.user_id == user_id)
        .filter(Temperatura.sujeto_id == sujeto_id)
        .all()
    )


def create(db_session: Session, *, temperatura_in: TemperaturaCreate) -> Temperatura:
    temperatura_in_data = jsonable_encoder(temperatura_in)
    temperatura = Temperatura(**temperatura_in_data)
    db_session.add(temperatura)
    db_session.commit()
    db_session.refresh(temperatura)
    log.debug(f"Created temperatura: {temperatura}")
    
    return temperatura