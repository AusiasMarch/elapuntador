import logging
import requests

import crud
from core import config


log = logging.getLogger('elapuntador')


def get_sujeto_place(sujeto):
    url_base = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    key = f"key={config.GOOGLE_API_KEY}"
    location = "location={},{}".format(
        *crud.coordinates.get_latlng_from_geom(sujeto.latlng))
    radius = "radius=1000"
    
    response = requests.get(url_base + "&".join([key, location, radius]))
    if response.status_code != 200:
        log.debug("Failed Google Place call.")
        return None
    loc_0 = response.json()['results'][0]['name']
    loc_1 = response.json()['results'][0]['vicinity']
    
    if loc_0 == "Igualada":
        return f"{loc_0} cerca de {loc_1}"
    else:
        return loc_1


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