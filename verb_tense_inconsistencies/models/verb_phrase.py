from dataclasses import dataclass
from spacy.tokens import Token


@dataclass
class VerbPhrase:

    token: Token

    auxiliaries: list[str]

    verb_tag: str    

    tense: str | None