from typing import Optional, List
from sqlalchemy.orm import Session
import pandas as pd

from fastapi.encoders import jsonable_encoder

from db_models.altura_who import Altura_Girls_Who
from db_models.altura_who import Altura_Boys_Who
from models.altura_who import AlturaWho


def get_all_girls(db_session: Session) -> pd.DataFrame:
    alturas_list = db_session.query(Altura_Girls_Who).all()

    alturas_who = pd.DataFrame(
        [(
            x.L,
            x.M,
            x.S,
            x.SD,
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
         alturas_list],
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
        index=[(x.day) for x in alturas_list]
    )

    return alturas_who


def create_girls(db_session: Session, *, altura_in: AlturaWho) -> Altura_Girls_Who:
    altura_in_data = jsonable_encoder(altura_in)
    altura_who = Altura_Girls_Who(**altura_in_data)
    db_session.add(altura_who)
    db_session.commit()
    db_session.refresh(altura_who)
    
    return altura_who


def get_all_boys(db_session: Session) -> pd.DataFrame:
    alturas_list = db_session.query(Altura_Boys_Who).all()

    alturas_who = pd.DataFrame(
        [(
            x.L,
            x.M,
            x.S,
            x.SD,
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
         alturas_list],
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
        index=[(x.day) for x in alturas_list]
    )

    return alturas_who


def create_boys(db_session: Session, *, altura_in: AlturaWho) -> Altura_Boys_Who:
    altura_in_data = jsonable_encoder(altura_in)
    altura_who = Altura_Boys_Who(**altura_in_data)
    db_session.add(altura_who)
    db_session.commit()
    db_session.refresh(altura_who)
    
    return altura_who