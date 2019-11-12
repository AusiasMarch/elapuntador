from pydantic import BaseModel
from typing import List


class ApunteResponse(BaseModel):
    # fulfillmentText: str
    payload: dict
    