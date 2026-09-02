from dataclasses import dataclass, field
from spacy.tokens import Span

from models.issue import Issue
from models.verb_phrase import VerbPhrase


@dataclass
class AnalysisContext:

    sentence: Span

    verb_phrases: list[VerbPhrase] = field(default_factory=list)

    advberbs: list[Span] = field(default_factory=list)

    issues: list[Issue] = field(default_factory=list)