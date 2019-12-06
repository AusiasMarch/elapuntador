import logging
import datetime

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
import crud
from api.utils.db import get_db
from models.temperatura import TemperaturaCreate
from models.msg import Msg
from core import config
from core import plots

from db.session import db_session


log = logging.getLogger('elapuntador')


router = APIRouter()

cyber_user = crud.user.get_by_name(db_session, name="Arduino")


@router.post("/", response_model=Msg, status_code=201)
def insert_temperature(
    *,
    body: dict,
    db_session: Session = Depends(get_db),
):
    log.debug(body)
    if body["secret_key"] != config.ARDUINO_API_KEY:
        log.debug(f"Temperature recived with api_key {body['secret_key']}.")
        return {"msg": "Not authorized."}
    apodo = body["sujeto"]
    grados = body["temperature"]
    humedad = body["humidity"]
    sujeto = crud.sujeto.get_by_apodo(db_session=db_session, apodo=apodo)
    temperatura_in = TemperaturaCreate(
        user_id=cyber_user.id,
        sujeto_id=sujeto.id,
        query_text=None,
        ip=None,
        grados=grados,
        decimas=0
    )
    crud.temperatura.create(db_session=db_session, temperatura_in=temperatura_in)
    _, last_temp = plots.get_last_static("temperatura", sujeto.name)

    if last_temp is None or \
            datetime.datetime.now() - last_temp > datetime.timedelta(hours=1):
        plots.plot_static("temperatura", sujeto.name)

    return {"msg": "Location updated."}

