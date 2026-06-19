

from model.lexicons import CLAUSAL_DEPS

# Roles de sujeto bajo los que puede aparecer "it"
_SUBJECT_DEPS = ("nsubj", "nsubjpass", "expl")

# Roles de sujeto (incluye sujetos clausales) para la detección personal
_SUBJECT_DEPS_FULL = ("nsubj", "nsubjpass", "csubj", "csubjpass", "expl")


def find_subject_it(sent):
    """Devuelve el token 'it' que funciona como sujeto, o None."""
    for tok in sent:
        if tok.lower_ == "it" and tok.dep_ in _SUBJECT_DEPS:
            return tok
    return None


def find_existential_there(sent):
    for tok in sent:
        if tok.lower_ == "there" and tok.dep_ == "expl":
            return tok
    return None


def has_extraposed_clause(anchor):
    for child in anchor.children:
        if child.dep_ in CLAUSAL_DEPS:
            marks = {c.lower_ for c in child.children}
            if "that" in marks or "to" in marks or child.pos_ in ("VERB", "AUX"):
                return True
        # "that" como mark directo colgando del ancla (parses alternativos)
        if child.dep_ == "mark" and child.lower_ == "that":
            return True
    return False


def get_acomp_or_attr(verb):
    for child in verb.children:
        if child.dep_ in ("acomp", "attr", "oprd") and child.pos_ in ("ADJ", "NOUN"):
            return child
    return None


def find_root(sent):
    """Devuelve el token raíz (ROOT) de la oración."""
    for tok in sent:
        if tok.dep_ == "ROOT":
            return tok
    return sent.root


def get_subject(verb):
    """Devuelve el sujeto sintáctico del verbo (incluye sujetos clausales y
    expletivos), o None. La regla que lo use decide qué hacer con él."""
    if verb is None:
        return None
    for child in verb.children:
        if child.dep_ in _SUBJECT_DEPS_FULL:
            return child
    return None
