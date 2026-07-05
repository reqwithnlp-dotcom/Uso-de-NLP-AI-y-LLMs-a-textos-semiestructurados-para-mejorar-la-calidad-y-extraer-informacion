from dataclasses import dataclass


@dataclass
class Issue:
    """
    Represents a detected verb tense inconsistency.
    """
        
    fragment: str
    position: int
    explanation: str
    error_code: str