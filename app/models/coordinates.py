from pydantic import BaseModel, validator


# https://github.com/tiangolo/fastapi/issues/315
# https://github.com/tiangolo/fastapi/issues/312
# https://gist.github.com/Sieboldianus/1d8f2f4b9d3519b640b695d62a28a6be

class Coordinates(BaseModel):
    lat: float = 0
    lng: float = 0
    
    @validator('lat')
    def lat_within_range(cls, v):
        if not -90 < v < 90:
            raise ValueError('Latitude outside allowed range')
        return v
    
    @validator('lng')
    def lng_within_range(cls, v):
        if not -180 < v < 180:
            raise ValueError('Longitude outside allowed range')
        return v
