from dataclasses import dataclass, field
from spacy.tokens import Span

from models.issue import Issue
from models.verb_features import VerbFeatures


@dataclass
class AnalysisContext:

    sentence: Span

    verb_features: list[VerbFeatures] = field(
        default_factory=list
    )

    advberbs: list[Span] = field(default_factory=list)
    
    issues: list[Issue] = field(
        default_factory=list
    )

    