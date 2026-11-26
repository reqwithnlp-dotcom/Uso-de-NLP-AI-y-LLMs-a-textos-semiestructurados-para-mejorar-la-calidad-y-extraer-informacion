"""
Capa 2: clasificador estadístico PERSONAL / IMPERSONAL (spaCy textcat_multilabel).

Solo se consulta para las oraciones que la capa 1 deja como `ambiguous`.
El modelo se entrena aparte (ver training/README.md) y se carga desde
disco. Si no hay modelo, `classify()` devuelve None y el servicio sigue
funcionando únicamente con la capa 1.

Configuración por variables de entorno:
    IMPERSONAL_TEXTCAT_PATH   carpeta del modelo (default: model/textcat)
    IMPERSONAL_L2_THRESHOLD   score mínimo de la clase ganadora (default 0.5)
    IMPERSONAL_L2_MARGIN      ventaja mínima sobre la otra clase (default 0.2)
"""

import os
from pathlib import Path

import spacy

LABELS = ("PERSONAL", "IMPERSONAL")
UNDECIDED = "UNDECIDED"

_DEFAULT_PATH = Path(__file__).resolve().parent / "textcat"

_textcat = None
_load_attempted = False


def model_path():
    return Path(os.environ.get("IMPERSONAL_TEXTCAT_PATH", _DEFAULT_PATH))


def _get_textcat():
    """Carga perezosa del modelo. Devuelve None si no está entrenado/copiado.
    Recuerda el resultado para no tocar el disco en cada oración."""
    global _textcat, _load_attempted
    if not _load_attempted:
        _load_attempted = True
        path = model_path()
        if (path / "config.cfg").exists():
            _textcat = spacy.load(path)
    return _textcat


def reset():
    """Olvida el modelo cargado (útil en tests o tras reemplazarlo en disco)."""
    global _textcat, _load_attempted
    _textcat, _load_attempted = None, False


def is_loaded():
    return _get_textcat() is not None


def classify(text):
    """Scores independientes {PERSONAL: p, IMPERSONAL: q}, o None sin modelo."""
    nlp = _get_textcat()
    if nlp is None:
        return None
    cats = nlp(text).cats
    return {lab: round(float(cats.get(lab, 0.0)), 4) for lab in LABELS}


def _env_float(name, default):
    try:
        return float(os.environ.get(name, default))
    except ValueError:
        return default


def decide(scores, threshold=None, margin=None):
    """Convierte los scores multilabel en una etiqueta.

    Gana la clase con mayor score si supera `threshold` Y le saca al menos
    `margin` a la otra. Si ambas son altas (contradictorio) o ambas bajas
    (sin evidencia), devuelve UNDECIDED: es la señal de caso límite que da
    textcat_multilabel y que se perdería con textcat exclusivo.
    """
    if not scores:
        return UNDECIDED
    threshold = _env_float("IMPERSONAL_L2_THRESHOLD", 0.5) if threshold is None else threshold
    margin = _env_float("IMPERSONAL_L2_MARGIN", 0.2) if margin is None else margin

    p, q = scores.get("PERSONAL", 0.0), scores.get("IMPERSONAL", 0.0)
    top_label, top, other = ("IMPERSONAL", q, p) if q >= p else ("PERSONAL", p, q)
    # round(): evita que 0.6 - 0.4 = 0.19999... quede por debajo de 0.2
    if top >= threshold and round(top - other, 6) >= margin:
        return top_label
    return UNDECIDED
