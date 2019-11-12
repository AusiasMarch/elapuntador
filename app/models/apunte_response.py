from pydantic import BaseModel
from typing import List


class ApunteResponse(BaseModel):
    expectUserResponse: str
    expectedInputs: List[dict]