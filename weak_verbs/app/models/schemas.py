from pydantic import BaseModel

class WeakVerbsRequest(BaseModel):
    text: str
