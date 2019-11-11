from typing import List, Optional

import crud

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from core.security import get_password_hash, verify_password
from db_models.sujeto import Sujeto
from models.sujeto import SujetoCreate

import pandas as pd


def create(db_session: Session, *, sujeto_in: SujetoCreate) -> Sujeto:
    sujeto_in.apodos.append(sujeto_in.name)
    sujeto = Sujeto(
        name=sujeto_in.name,
        apodos=sujeto_in.apodos,
        birth=sujeto_in.birth
    )
    db_session.add(sujeto)
    db_session.commit()
    db_session.refresh(sujeto)
    return sujeto


def get_all(db_session: Session) -> pd.DataFrame:
    sujetos_list = db_session.query(Sujeto).all()

    sujetos = pd.DataFrame(
        [(x.name, x.apodos, x.birth) for x in
         sujetos_list],
        columns=['name', 'apodos', 'birth'],
        index=[(x.id) for x in sujetos_list]
    )

    return sujetos


def get_by_name(db_session: Session, *, sujeto_name: int) -> Optional[Sujeto]:
    return db_session.query(Sujeto).filter(Sujeto.name == sujeto_name).first()


def get_by_id(db_session: Session, *, sujeto_id: int) -> Optional[Sujeto]:
    return db_session.query(Sujeto).filter(Sujeto.id == sujeto_id).first()


def get_by_apodo(db_session: Session, *, apodo: str) -> Optional[Sujeto]:
    return db_session.query(Sujeto).filter(Sujeto.apodos.any(apodo.lower())).first()
