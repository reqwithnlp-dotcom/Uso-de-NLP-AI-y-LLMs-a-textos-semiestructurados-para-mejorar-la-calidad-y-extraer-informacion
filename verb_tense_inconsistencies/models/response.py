from pydantic import BaseModel


class IssueResponse(BaseModel):
    fragment: str
    position: int
    explanation: str
    error_code: str


class AnalyzeResponse(BaseModel):

    normalized_text: str

    fragments: list[str]

    issues: list[IssueResponse]