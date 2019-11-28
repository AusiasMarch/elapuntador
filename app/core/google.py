import logging
import requests

import crud
from core import config


log = logging.getLogger('elapuntador')

"""
from db.session import db_session
from models.coordinates import Coordinates

sujeto=crud.sujeto.get_by_apodo(db_session=db_session, apodo="Ausias")
coordinates = Coordinates(lat=41.549812, lng=1.847321) # A2
coordinates = Coordinates(lat=41.584295, lng=1.624064) # Avda Barcelona
crud.sujeto.update_latlng(db_session=db_session, sujeto=sujeto, coordinates=coordinates, car=True)
"""

def get_sujeto_place(sujeto):
    url_base = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    key = f"key={config.GOOGLE_API_KEY}"
    location = "location={},{}".format(
        *crud.coordinates.get_latlng_from_geom(sujeto.latlng))
    radius = "radius=1000"
    
    url = url_base + "&".join([key, location, radius])
    response = requests.get(url)
    if response.status_code != 200:
        log.debug("Failed Google Place call.")
        return None
    elif len(response.json()['results']) == 0:
        log.debug("No results found.")
        log.debug(url)
        return None
    loc_0 = response.json()['results'][0]
    loc_1 = response.json()['results'][1]
    if loc_0["name"] == "Igualada":
        return f"{loc_0['name']} cerca de {loc_1['vicinity']}"
    else:
        for loc in response.json()['results']:
            if 'locality' in loc["types"]:
                return loc["name"]
    return f"near {loc_0['vicinity'].split(',')[-1].strip()}"


def get_expected_time(sujeto_1, sujeto_2):
    url_base = "https://maps.googleapis.com/maps/api/directions/json?"
    key = f"key={config.GOOGLE_API_KEY}"
    origin = "origin={},{}".format(
        *crud.coordinates.get_latlng_from_geom(sujeto_1.latlng))
    destination = "destination={},{}".format(
        *crud.coordinates.get_latlng_from_geom(sujeto_2.latlng))

    response = requests.get(url_base + "&".join([key, origin, destination]))
    if response.status_code != 200:
        return None
    return response.json()["routes"][0]["legs"][0]["duration"]["value"]