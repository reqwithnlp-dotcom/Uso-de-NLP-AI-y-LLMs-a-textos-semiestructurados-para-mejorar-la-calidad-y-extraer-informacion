from pydantic import BaseModel


class DetectRequest(BaseModel):
    text: str


class DetectResponse(BaseModel):
    unusual_punctuation: bool
    positions: list[str] | int