from dataclasses import dataclass, field
from typing import Any

from models.verb_classification_type import VerbClassificationType


@dataclass(frozen=True)
class VerbClassification:
    classification_type: VerbClassificationType
    value: str    