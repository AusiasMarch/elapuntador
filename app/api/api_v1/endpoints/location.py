import logging

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
import crud
from api.utils.db import get_db
from models.msg import Msg
from models.coordinates import Coordinates


log = logging.getLogger('elapuntador')


router = APIRouter()


@router.post("/", response_model=Msg, status_code=201)
def insert_apunte(
    *,
    body: dict,
    x_forwarded_for: str = Header(None),
    db_session: Session = Depends(get_db),
):
    print(body)
    log.debug(body)
    # apodo =
    # lat =
    # lng =
    # sujeto = crud.sujeto.get_by_apodo(db_session=db_session, apodo=apodo)
    # coordinates = Coordinates(lat=lat, lng=lng)
    # crud.sujeto.update_latlng(db_session=db_session, sujeto=sujeto,
    #                           coordinates=coordinates, car=False)

    return {"msg": "Location saved"}