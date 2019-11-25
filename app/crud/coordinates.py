from typing import Union
from geoalchemy2 import WKTElement
from geoalchemy2.shape import to_shape

from models.coordinates import Coordinates


def get_geom_from_coordinates(coords: Coordinates) -> str:
    geom_wkte = f'SRID=4326;POINT({coords.lng} {coords.lat})'
    return geom_wkte


def get_point_from_wkte(coords: WKTElement) -> str:
    geom_wkte = f'SRID=4326;POINT({coords.lng} {coords.lat})'
    return geom_wkte


def get_coordinates_from_geom(geom: WKTElement) -> Coordinates:
    sahply_geom = to_shape(geom)
    coordinates = Coordinates(lng=sahply_geom.x, lat=sahply_geom.y)
    return coordinates


def get_latlng_from_geom(geom: Union[WKTElement, Coordinates] = None):
    if geom is None:
        return None, None
    sahply_geom = to_shape(geom)
    return sahply_geom.y, sahply_geom.x