from pydantic import BaseModel
from typing import List


class ApunteResponse(BaseModel):
    fulfillmentText: str
    fulfillmentMessages: List[dict]
    source: str
    payload: dict
    