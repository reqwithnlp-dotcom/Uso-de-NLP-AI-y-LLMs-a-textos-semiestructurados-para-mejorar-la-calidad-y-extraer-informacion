import spacy

from model.rules import RULES, DEFAULT_TYPE

_MODEL_NAME = "en_core_web_sm"
_nlp = None


def _get_nlp():
    
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load(_MODEL_NAME)
        except OSError as exc:
            raise RuntimeError(
                f"El modelo de spaCy '{_MODEL_NAME}' no está instalado. "
                f"Ejecutá: python -m spacy download {_MODEL_NAME}"
            ) from exc
    return _nlp


def analyze_sentence(sent):
    
    for rule in RULES:
        detected = rule(sent)
        if detected is not None:
            return {
                "sentence": sent.text.strip(),
                "impersonal": True,
                "type": detected,
            }
    return {
        "sentence": sent.text.strip(),
        "impersonal": False,
        "type": DEFAULT_TYPE,
    }


def analyze_text(text):
   
    if not text or not text.strip():
        return []
    doc = _get_nlp()(text)
    return [analyze_sentence(sent) for sent in doc.sents]
