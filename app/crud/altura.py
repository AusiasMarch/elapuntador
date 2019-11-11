from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from db_models.altura import Altura
from models.altura import AlturaCreate

import pandas as pd

def get_by_id(db_session: Session, *, altura_id: int) -> Optional[Altura]:
    return db_session.query(Altura).filter(Altura.id == altura_id).first()


def get_all(db_session: Session) -> pd.DataFrame:
    alturas_list = db_session.query(Altura).all()

    alturas = pd.DataFrame(
        [(x.datetime, x.centimetros, x.ip, x.user_id, x.user.full_name) for x in
         alturas_list],
        columns=['datetime', 'centimetros', 'ip', 'user_id', 'user_name'],
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


def create(db_session: Session, *, altura_in: AlturaCreate) -> Altura:
    altura_in_data = jsonable_encoder(altura_in)
    altura = Altura(**altura_in_data)
    db_session.add(altura)
    db_session.commit()
    db_session.refresh(altura)
    
    return altura