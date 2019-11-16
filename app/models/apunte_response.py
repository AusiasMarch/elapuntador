from pydantic import BaseModel
from typing import List


class ApunteResponse(BaseModel):
    payload: dict
    