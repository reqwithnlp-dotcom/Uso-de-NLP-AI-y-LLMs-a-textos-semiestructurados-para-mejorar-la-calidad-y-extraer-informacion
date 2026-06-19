import spacy

from model.rules import IMPERSONAL_RULES, PERSONAL_RULES, DEFAULT_TYPE

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


def _first_match(rules, sent):
    """Devuelve el subtipo de la primera regla que matchea, o None."""
    for rule in rules:
        detected = rule(sent)
        if detected is not None:
            return detected
    return None


def analyze_sentence(sent):
    """Capa 1 del pipeline. Corre dos baterías de reglas INDEPENDIENTES y
    devuelve dos booleanos: «es personal» y «es impersonal».

    - Caso limpio: exactamente uno es True (sin dudas).
    - Caso límite / contradictorio: ambos True o ambos False -> `ambiguous`
      queda en True y la oración debe escalar a la capa 2 (LLM).
    """
    impersonal_type = _first_match(IMPERSONAL_RULES, sent)
    personal_type = _first_match(PERSONAL_RULES, sent)

    is_impersonal = impersonal_type is not None
    is_personal = personal_type is not None

    return {
        "sentence": sent.text.strip(),
        "personal": is_personal,        # «Es personal»
        "impersonal": is_impersonal,    # «Es impersonal»
        # Caso límite: misma respuesta en ambos detectores -> capa 2
        "ambiguous": is_personal == is_impersonal,
        "type": impersonal_type or DEFAULT_TYPE,   # subtipo impersonal
        "personal_type": personal_type,            # subtipo personal o None
    }


def analyze_text(text):
   
    if not text or not text.strip():
        return []
    doc = _get_nlp()(text)
    return [analyze_sentence(sent) for sent in doc.sents]
