from dataclasses import dataclass


@dataclass
class SentenceFragment:
    text: str
    doc: any  # spacy.Doc or spacy.Span
    start_char: int
    end_char: int