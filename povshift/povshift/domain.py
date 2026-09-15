from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Character:
    id: int
    canonical_name: str
    mentions: list[str] = field(default_factory=list)


@dataclass
class Clause:
    text: str
    sentence_index: int
    subject: Optional[Character] = None
    verb: Optional[str] = None
    internal_state: bool = False
    state_type: Optional[str] = None
    experiencer: Optional[Character] = None


@dataclass
class FocusState:
    character: Optional[Character]
    sentence_index: int
    reason: Optional[str] = None


@dataclass
class POVShift:
    from_character: Character
    to_character: Character
    sentence_index: int
    confidence: float
    evidence: list[str] = field(default_factory=list)
