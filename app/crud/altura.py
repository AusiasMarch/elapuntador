import logging

from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from db_models.altura import Altura
from models.altura import AlturaCreate

import pandas as pd


log = logging.getLogger("elapuntador")


def get_by_id(db_session: Session, *, altura_id: int) -> Optional[Altura]:
    altura = db_session.query(Altura).filter(Altura.id == altura_id).first()
    log.debug(f"Altura got by id: {altura}")
    return altura


def get_all(db_session: Session) -> pd.DataFrame:
    alturas_list = db_session.query(Altura).all()

    alturas = pd.DataFrame(
        [(x.datetime, x.sujeto_id, x.sujeto.name, x.centimetros, x.ip, x.user_id, x.user.full_name) for x in
         alturas_list],
        columns=['datetime', 'sujeto_id', 'sujeto', 'centimetros', 'ip', 'user_id', 'user_name'],
        index=[(x.id) for x in alturas_list]
    )

    return alturas


def get_all_by_user(
    db_session: Session, *, user_id: int
) -> List[Optional[Altura]]:
    return (
        db_session.query(Altura)
        .filter(Altura.user_id == user_id)
        .all()
    )


def get_all_by_sujeto(
    db_session: Session, *, sujeto_id: int
) -> pd.DataFrame:
    alturas_list = db_session.query(
        Altura
    ).filter(
        Altura.sujeto_id == sujeto_id
    ).all()

    alturas = pd.DataFrame(
        [(x.datetime, x.centimetros, x.ip, x.user_id, x.user.full_name) for x in
         alturas_list],
        columns=['datetime', 'centimetros', 'ip', 'user_id', 'user_name'],
        index=[(x.id) for x in alturas_list]
    )
    
    return alturas


def get_all_by_user_and_sujeto(
    db_session: Session, *, user_id: int, sujeto_id: int
) -> pd.DataFrame:
    alturas_list = db_session.query(
        Altura
    ).filter(
        Altura.user_id == user_id
    ).filter(
        Altura.sujeto_id == sujeto_id
    ).all()

    alturas = pd.DataFrame(
        [(x.datetime, x.sujeto_id, x.sujeto.name, x.centimetros, x.ip, x.user_id, x.user.full_name) for x in
         alturas_list],
        columns=['datetime', 'sujeto_id', 'sujeto', 'centimetros', 'ip', 'user_id', 'user_name'],
        index=[(x.id) for x in alturas_list]
    )
    
    
    return alturas


def create(db_session: Session, *, altura_in: AlturaCreate) -> Altura:
    altura_in_data = jsonable_encoder(altura_in)
    altura = Altura(**altura_in_data)
    db_session.add(altura)
    db_session.commit()
    db_session.refresh(altura)
    log.debug(f"Created altura: {altura}")
    
    return altura