import spacy

from model import classifier
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


def _resolve(sent, is_personal, is_impersonal, ambiguous, use_layer2=True):
    """Decisión final. Capa 1 si fue clara; si no, capa 2 (si hay modelo)."""
    if not ambiguous:
        label = "IMPERSONAL" if is_impersonal else "PERSONAL"
        return label, "layer1", None

    scores = classifier.classify(sent.text.strip()) if use_layer2 else None
    if scores is None:
        return classifier.UNDECIDED, "none", None
    label = classifier.decide(scores)
    return label, ("layer2" if label != classifier.UNDECIDED else "none"), scores


def analyze_sentence(sent, use_layer2=True):
    """Pipeline por oración.

    Capa 1: dos baterías de reglas INDEPENDIENTES -> «es personal» y
    «es impersonal».
    - Caso limpio: exactamente uno es True (decide la capa 1).
    - Caso límite / contradictorio: ambos True o ambos False -> `ambiguous`
      y se consulta la capa 2 (clasificador spaCy entrenado, model/classifier).

    `use_layer2=False` corre solo la capa 1 (lo usan los scripts de
    training/ para medir el baseline sin cargar el clasificador).
    """
    impersonal_type = _first_match(IMPERSONAL_RULES, sent)
    personal_type = _first_match(PERSONAL_RULES, sent)

    is_impersonal = impersonal_type is not None
    is_personal = personal_type is not None
    ambiguous = is_personal == is_impersonal

    final_label, decided_by, layer2_scores = _resolve(
        sent, is_personal, is_impersonal, ambiguous, use_layer2
    )

    return {
        "sentence": sent.text.strip(),
        "personal": is_personal,        # «Es personal»
        "impersonal": is_impersonal,    # «Es impersonal»
        # Caso límite: misma respuesta en ambos detectores -> capa 2
        "ambiguous": ambiguous,
        "type": impersonal_type or DEFAULT_TYPE,   # subtipo impersonal
        "personal_type": personal_type,            # subtipo personal o None
        # Decisión final del pipeline (capa 1 + capa 2)
        "final_label": final_label,      # PERSONAL | IMPERSONAL | UNDECIDED
        "decided_by": decided_by,        # layer1 | layer2 | none
        "layer2_scores": layer2_scores,  # {PERSONAL, IMPERSONAL} o None
    }


def analyze_text(text):
   
    if not text or not text.strip():
        return []
    doc = _get_nlp()(text)
    return [analyze_sentence(sent) for sent in doc.sents]
