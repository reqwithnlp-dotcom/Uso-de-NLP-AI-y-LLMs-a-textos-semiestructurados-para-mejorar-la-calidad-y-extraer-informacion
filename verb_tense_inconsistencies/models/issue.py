from dataclasses import dataclass


@dataclass
class Issue:
    fragment: str
    position: int
    explanation: str
    error_code: str