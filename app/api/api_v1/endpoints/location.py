import logging

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
import crud
from api.utils.db import get_db
from models.msg import Msg
from models.coordinates import Coordinates
from core import config


log = logging.getLogger('elapuntador')


router = APIRouter()


@router.post("/", response_model=Msg, status_code=201)
def insert_location(
    *,
    body: dict,
    db_session: Session = Depends(get_db),
):
    if body["api_key"] != config.TASKER_API_KEY:
        log.debug(f"Location recived with api_key {body['api_key']}.")
        return {"msg": "Not authorized."}
    log.debug(body)
    apodo = body["sujeto"]
    lat, lng = body["location"].split(",")
    lat = float(lat)
    lng = float(lng)
    sujeto = crud.sujeto.get_by_apodo(db_session=db_session, apodo=apodo)
    log.debug(sujeto)
    coordinates = Coordinates(lat=lat, lng=lng)
    log.debug(coordinates)
    crud.sujeto.update_latlng(db_session=db_session, sujeto=sujeto,
                              coordinates=coordinates, car=False)
    log.debug(f"Location updated for user {sujeto.name}")
    return {"msg": "Location saved"}