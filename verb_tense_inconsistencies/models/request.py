from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    text: str