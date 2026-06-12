from pydantic import BaseModel
from typing import List


class PerceptionOpinionRequest(BaseModel):
    text: str


class PerceptionOpinionResponse(BaseModel):
    opinion_perception: List[str]
    others: List[str]