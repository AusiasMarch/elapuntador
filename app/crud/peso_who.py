from typing import Optional, List
from sqlalchemy.orm import Session
import pandas as pd

from fastapi.encoders import jsonable_encoder

from db_models.peso_who import Peso_Girls_Who
from db_models.peso_who import Peso_Boys_Who
from models.peso_who import PesoWho


def get_all_girls(db_session: Session) -> pd.DataFrame:
    pesos_list = db_session.query(Peso_Girls_Who).all()

    pesos_who = pd.DataFrame(
        [(
            x.L,
            x.M,
            x.S,
            x.P01,
            x.P1,
            x.P3,
            x.P5,
            x.P10,
            x.P15,
            x.P25,
            x.P50,
            x.P75,
            x.P85,
            x.P90,
            x.P95,
            x.P97,
            x.P99,
            x.P999,
        ) for x in
         pesos_list],
        columns=[
            'L',
            'M',
            'S',
            'SD',
            'P01',
            'P1',
            'P3',
            'P5',
            'P10',
            'P15',
            'P25',
            'P50',
            'P75',
            'P85',
            'P90',
            'P95',
            'P97',
            'P99',
            'P999',
        ],
        index=[(x.day) for x in pesos_list]
    )

    return pesos_who


def create_girls(db_session: Session, *, peso_in: PesoWho) -> Peso_Girls_Who:
    peso_in_data = jsonable_encoder(peso_in)
    peso_who = Peso_Girls_Who(**peso_in_data)
    db_session.add(peso_who)
    db_session.commit()
    db_session.refresh(peso_who)
    
    return peso_who


def get_all_boys(db_session: Session) -> pd.DataFrame:
    pesos_list = db_session.query(Peso_Boys_Who).all()

    pesos_who = pd.DataFrame(
        [(
            x.L,
            x.M,
            x.S,
            x.P01,
            x.P1,
            x.P3,
            x.P5,
            x.P10,
            x.P15,
            x.P25,
            x.P50,
            x.P75,
            x.P85,
            x.P90,
            x.P95,
            x.P97,
            x.P99,
            x.P999,
        ) for x in
         pesos_list],
        columns=[
            'L',
            'M',
            'S',
            'SD',
            'P01',
            'P1',
            'P3',
            'P5',
            'P10',
            'P15',
            'P25',
            'P50',
            'P75',
            'P85',
            'P90',
            'P95',
            'P97',
            'P99',
            'P999',
        ],
        index=[(x.day) for x in pesos_list]
    )

    return pesos_who


def create_boys(db_session: Session, *, peso_in: PesoWho) -> Peso_Boys_Who:
    peso_in_data = jsonable_encoder(peso_in)
    peso_who = Peso_Boys_Who(**peso_in_data)
    db_session.add(peso_who)
    db_session.commit()
    db_session.refresh(peso_who)
    
    return peso_who