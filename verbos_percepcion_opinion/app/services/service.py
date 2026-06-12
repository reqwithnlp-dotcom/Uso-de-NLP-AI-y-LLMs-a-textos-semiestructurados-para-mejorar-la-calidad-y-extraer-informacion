"""verbos_percepcion_opinion.service

Function to detect opinion and perception verbs in English text.
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

OPINION_AND_PERCEPTION_VERBS = [
    "think",
    "believe",
    "know",
    "understand",
    "guess",
    "expect",
    "consider",
    "suppose",
    "imagine",
    "agree",
    "disagree",
    "doubt",
    "feel",
    "perceive",
    "see",
    "hear",
    "smell",
    "taste",
    "notice",
    "realize",
    "remember",
    "forget",
]



def detect_opinion_and_perception(text: str) -> Dict[str, List[str]]:
    """Detect opinion and perception verbs in `text`.

    Returns a dict with two keys:
    - "opinion_perception": list of tokens (original text) that are verbs and whose lemma is
      in the target list.
    - "others": list of tokens that do not meet the above condition.

    If `nlp` is not available, classify all words as "others".
    """
    result = {"opinion_perception": [], "others": []}

    if nlp is None:
        for token_text in re.findall(r"\w+", text, flags=re.UNICODE):
            result["others"].append(token_text)
        return result

    doc = nlp(text)
    for token in doc:
        if token.is_punct:
            continue
        if (
            token.pos_ == "VERB"
            and token.lemma_.lower() in OPINION_AND_PERCEPTION_VERBS
        ):
            result["opinion_perception"].append(token.text)
        else:
            result["others"].append(token.text)

    return result