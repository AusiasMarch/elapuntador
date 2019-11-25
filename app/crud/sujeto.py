import logging
import re
import datetime
from unicodedata import normalize
import pandas as pd
from typing import Optional

import crud

from sqlalchemy.orm import Session


from db_models.sujeto import Sujeto
from models.sujeto import SujetoCreate, SujetoInDB
from models.coordinates import Coordinates


log = logging.getLogger("elapuntador")


def create(db_session: Session, *, sujeto_in: SujetoCreate) -> Sujeto:
    sujeto_in.apodos.append(sujeto_in.name)
    extra_apodos = set()
    for apodo in sujeto_in.apodos:
        variantes = [
            apodo.lower(),
            re.sub(
                r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+",
                r"\1",
                normalize("NFD", apodo), 0, re.I
            ),
            re.sub(
                r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+",
                r"\1",
                normalize("NFD", apodo), 0, re.I
            ).lower(),
        ]
        for variante in variantes:
            if variante not in sujeto_in.apodos:
                extra_apodos.add(variante)
    sujeto_in.apodos.extend(list(extra_apodos))
    
    sujeto = Sujeto(
        name=sujeto_in.name,
        gender=sujeto_in.gender,
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
        [(x.name, x.gender, x.apodos, x.birth, x.latlng, x.latlng_update, x.latlng_car) for x in
         sujetos_list],
        columns=['name', 'gender', 'apodos', 'birth', 'latlng', 'latlng_update', 'latlng_car'],
        index=[(x.id) for x in sujetos_list]
    )
    sujetos['latlng'] = sujetos['latlng'].apply(crud.coordinates.get_latlng_from_geom)
    sujetos[['lat', 'lng']] = pd.DataFrame(sujetos['latlng'].tolist(), index=sujetos.index)

    return sujetos


def get_by_name(db_session: Session, *, name: str) -> Optional[Sujeto]:
    sujeto = db_session.query(Sujeto).filter(Sujeto.name == name).first()
    log.debug(f"Sujeto got by name: {sujeto}")
    return sujeto


def get_by_id(db_session: Session, *, sujeto_id: int) -> Optional[Sujeto]:
    sujeto = db_session.query(Sujeto).filter(Sujeto.id == sujeto_id).first()
    log.debug(f"Sujeto got from id: {sujeto}")
    return sujeto


def get_by_apodo(db_session: Session, *, apodo: str) -> Optional[Sujeto]:
    sujeto = db_session.query(Sujeto).filter(Sujeto.apodos.any(apodo)).first()
    log.debug(f"Sujeto got from apodo: {sujeto}")
    return sujeto


def update_latlng(
        db_session: Session, *,
        sujeto: SujetoInDB,
        coordinates: Coordinates,
        car: bool
) -> None:
    coordinates_geom = crud.coordinates.get_geom_from_coordinates(coordinates)
    db_session.query(Sujeto). \
        filter(Sujeto.id == sujeto.id). \
        update(
        {
            "latlng": coordinates_geom,
            "latlng_update": datetime.datetime.utcnow(),
            "latlng_car": car
        }
    )
    db_session.commit()