import logging
import requests

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from db_models.location import Location
from models.location import LocationCreate, LocationInDb
from models.sujeto import SujetoInDB
import crud


log = logging.getLogger("elapuntador")


def get_by_id(db_session: Session, *, location_id: int) -> Optional[Location]:
    location = db_session.query(Location).filter(Location.id == location_id).first()
    log.debug(f"Location got by id: {location}")
    return location


def get_by_name(db_session: Session, *, location_name: str) -> Optional[Location]:
    location = db_session.query(Location).filter(Location.name == location_name).first()
    log.debug(f"Location got by name: {location}")
    return location


def get_all(db_session: Session) -> List[Optional[Location]]:
    return db_session.query(Location).all()

"""
from db.session import db_session
sujeto=crud.sujeto.get_by_name(db_session=db_session, name="Entropía")
"""
def get_by_sujeto(
    db_session: Session, *, sujeto: SujetoInDB
) -> Optional[Location]:
    if sujeto.latlng is not None:
        location = db_session.query(Location).filter(
            func.ST_Contains(
                func.ST_Buffer(
                    func.ST_Transform(
                        Location.center,
                        32631
                    ),
                    Location.radius
                ),
                func.ST_Transform(
                    func.ST_GeomFromEWKT(
                        'SRID=4326;POINT({} {})'.format(
                            *crud.coordinates.get_latlng_from_geom(sujeto.latlng)[::-1])
                    ),
                    32631
                )
            )
        ).order_by(
            func.ST_Transform(
                Location.center,
                32631
            ).ST_Buffer(Location.radius).ST_Area().asc()).first()
        if location is not None:
            return location.name
        else:
            url_base = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
            key = "key=AIzaSyCdCiYs_Q_KHP_GG1xLJwYYPPSO3yFRilg"
            location = 'location={},{}'.format(
                *crud.coordinates.get_latlng_from_geom(sujeto.latlng))
            radius = 'radius=1000'
    
            response = requests.get(url_base + "&".join([key, location, radius]))
            return response.json()['results'][0]['name']
    else:
        return None


def create(db_session: Session, *, location_in: LocationCreate) -> LocationInDb:
    location_in_db = Location(
        name=location_in.name,
        center=crud.coordinates.get_geom_from_coordinates(location_in.center),
        radius=location_in.radius
    )
    db_session.add(location_in_db)
    db_session.commit()
    db_session.refresh(location_in_db)
    log.debug(f"Created location: {location_in_db}")

    return location_in_db
