"""
Detector de oraciones impersonales en inglés (spaCy).

Pipeline:
    1. Recibir texto.
    2. Procesar con spaCy (tokeniza, POS, lemma, dependency parse, sentencizer).
    3. Separar en oraciones (doc.sents).
    4. Para cada oracion, aplicar las reglas EN ORDEN y cortar en la primera que matchea:
         THERE_EXISTENTIAL -> WEATHER_IT -> WEATHER_ADJECTIVE
         -> IMPERSONAL_PASSIVE -> IT_EXTRAPOSITION -> REFERENTIAL_IT (False)
    5. Devolver lista de dicts: {sentence, impersonal, type}

Nota importante sobre spaCy:
    - "there" existencial: spaCy lo etiqueta de forma confiable como dep_ == "expl".
    - "it" expletivo: spaCy lo suele etiquetar como "nsubj", NO como "expl".
      Por eso para "it" NO alcanza la etiqueta de dependencia: se cruza con
      lexico (clima / verbos de reporte) y con la estructura (cláusula extrapuesta).
"""

import spacy

nlp = spacy.load("en_core_web_sm")

# ---------------------------------------------------------------------------
# Lexicones (ajustables / ampliables)
# ---------------------------------------------------------------------------
WEATHER_VERBS = {
    "rain", "snow", "drizzle", "hail", "thunder", "pour",
    "sleet", "freeze", "storm", "lighten",
}
WEATHER_ADJ = {
    "cold", "hot", "warm", "cool", "sunny", "rainy", "cloudy", "windy",
    "foggy", "snowy", "humid", "chilly", "freezing", "boiling", "stormy",
    "dark", "bright", "overcast", "muggy", "icy",
}
REPORTING_VERBS = {
    "say", "believe", "think", "report", "know", "expect", "claim",
    "suggest", "assume", "estimate", "allege", "rumor", "argue",
    "hope", "agree", "understand", "feel",
}
COPULAR_VERBS = {"be", "seem", "appear", "look", "happen"}
CLAUSAL_DEPS = {"xcomp", "ccomp", "advcl", "csubj", "acl"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _find_it(sent):
    """Devuelve el token 'it' que funciona como sujeto, o None."""
    for tok in sent:
        if tok.lower_ == "it" and tok.dep_ in ("nsubj", "expl", "nsubjpass"):
            return tok
    return None


def _find_there(sent):
    """Devuelve el token 'there' existencial (expl), o None."""
    for tok in sent:
        if tok.lower_ == "there" and tok.dep_ == "expl":
            return tok
    return None


def _has_extraposed_clause(anchor):
    """¿El ancla (verbo o adjetivo) arrastra una cláusula subordinada con
    marca 'to' o 'that'? Esa cláusula es el 'sujeto real' desplazado."""
    for child in anchor.children:
        if child.dep_ in CLAUSAL_DEPS:
            marks = {c.lower_ for c in child.children}
            if "that" in marks or "to" in marks:
                return True
    return False


# ---------------------------------------------------------------------------
# Reglas (cada una devuelve el nombre del tipo si matchea, o None)
# ---------------------------------------------------------------------------
def rule_there_existential(sent):
    there = _find_there(sent)
    if there and there.head.lemma_ == "be":
        return "THERE_EXISTENTIAL"
    return None


def rule_weather_it(sent):
    it = _find_it(sent)
    if it and it.head.lemma_ in WEATHER_VERBS:
        return "WEATHER_IT"
    return None


def rule_weather_adjective(sent):
    it = _find_it(sent)
    if not it or it.head.lemma_ not in COPULAR_VERBS:
        return None
    verb = it.head
    for child in verb.children:
        if child.dep_ == "acomp" and child.lemma_ in WEATHER_ADJ:
            return "WEATHER_ADJECTIVE"
    return None


def rule_impersonal_passive(sent):
    it = _find_it(sent)
    if not it:
        return None
    verb = it.head
    # it + be + participio pasado (+ cláusula that)
    for child in verb.children:
        if child.tag_ == "VBN":
            if _has_extraposed_clause(verb) or _has_extraposed_clause(child):
                return "IMPERSONAL_PASSIVE"
    # caso "It is said that ..." donde el participio es la raiz
    if verb.tag_ == "VBN" and _has_extraposed_clause(verb):
        return "IMPERSONAL_PASSIVE"
    return None


def rule_it_extraposition(sent):
    it = _find_it(sent)
    if not it or it.head.lemma_ not in COPULAR_VERBS:
        return None
    verb = it.head
    # it + (be/seem/appear) + adjetivo + CLÁUSULA extrapuesta
    adj = next((c for c in verb.children if c.dep_ == "acomp"), None)
    if adj and (_has_extraposed_clause(adj) or _has_extraposed_clause(verb)):
        return "IT_EXTRAPOSITION"
    # "It seems that ..." sin adjetivo
    if verb.lemma_ in {"seem", "appear"} and _has_extraposed_clause(verb):
        return "IT_EXTRAPOSITION"
    return None


RULES = [
    rule_there_existential,
    rule_weather_it,
    rule_weather_adjective,
    rule_impersonal_passive,
    rule_it_extraposition,
]


# ---------------------------------------------------------------------------
# API publica
# ---------------------------------------------------------------------------
def analyze_sentence(sent):
    for rule in RULES:
        result = rule(sent)
        if result:
            return {"sentence": sent.text.strip(), "impersonal": True, "type": result}
    return {"sentence": sent.text.strip(), "impersonal": False, "type": "NOT_IMPERSONAL"}


def analyze_text(text):
    doc = nlp(text)
    return [analyze_sentence(sent) for sent in doc.sents]


# ---------------------------------------------------------------------------
# Demo con los ejemplos del documento
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    demo = (
        "It is important to remember the guidelines. "
        "There are many factors to consider. "
        "It rains a lot. "
        "It is cold today. "
        "It is said that history repeats itself. "
        "I bought a car. It is fast. "
        "It seems that the results are wrong."
    )
    for r in analyze_text(demo):
        flag = "IMPERSONAL" if r["impersonal"] else "personal  "
        print(f"[{flag}] {r['type']:<20} | {r['sentence']}")