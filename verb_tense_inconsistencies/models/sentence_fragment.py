from dataclasses import dataclass


@dataclass
class SentenceFragment:
    text: str
    start_char: int
    end_char: int