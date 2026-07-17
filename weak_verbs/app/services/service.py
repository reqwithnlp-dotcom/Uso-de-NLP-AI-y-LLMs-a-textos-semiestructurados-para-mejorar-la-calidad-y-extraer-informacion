"""Weak_verbs_service

Function to detect weak verbs in English text.
"""

import re
from typing import Dict, List

try:
    import spacy
except Exception:
    spacy = None

try:
    nlp = spacy.load("en_core_web_sm") if spacy is not None else None
except Exception as exc:
    raise RuntimeError("Could not load spaCy model 'en_core_web_sm'") from exc

WEAK_VERBS = [
    "do",
    "make",
    "have",
    "get",
    "take",
    "give",
    "go",
    "run",
    "keep",
    "play",
    "put",
    "set",
    "be"
]


def detect_weak_verbs(text: str) -> List[str]:
    """Detect weak verbs in 'text'
    Return a list with verbs in case that 'text' contains weak_verbs,
    excluding those that are part of a phrasal verb.
    """
    weak_verbs_found = []

    if nlp is None:
        return weak_verbs_found
    
    doc = nlp(text)
    for token in doc:
        if token.pos_ in ("VERB", "AUX") and token.lemma_ in WEAK_VERBS:

            # Verify if it has a particle child (prt) to exclude phrasal verbs (dep_ == "prt")
            is_phrasal = any(child.dep_ == "prt" for child in token.children)

            if not is_phrasal:
                weak_verbs_found.append(token.text)
    return weak_verbs_found