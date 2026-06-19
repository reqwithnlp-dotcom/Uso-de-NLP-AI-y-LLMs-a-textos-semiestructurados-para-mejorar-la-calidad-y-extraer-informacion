"""
Lexicones del detector de oraciones impersonales.

Estos diccionarios léxicos alimentan a las reglas de `rules.py`.
Se mantienen aislados para poder ampliarlos sin tocar la lógica.
"""

# Verbos meteorológicos: "It rains", "It snowed", "It is pouring"
WEATHER_VERBS = frozenset({
    "rain", "snow", "drizzle", "hail", "thunder", "pour",
    "sleet", "freeze", "storm", "lighten", "mist", "shower",
})

# Adjetivos de clima/ambiente: "It is cold", "It was foggy"
WEATHER_ADJECTIVES = frozenset({
    "cold", "hot", "warm", "cool", "sunny", "rainy", "cloudy", "windy",
    "foggy", "snowy", "humid", "chilly", "freezing", "boiling", "stormy",
    "dark", "bright", "overcast", "muggy", "icy", "wet", "dry", "breezy",
    "late", "early", 
})


REPORTING_VERBS = frozenset({
    "say", "believe", "think", "report", "know", "expect", "claim",
    "suggest", "assume", "estimate", "allege", "rumor", "argue",
    "hope", "agree", "understand", "feel", "consider", "acknowledge",
    "announce", "reveal",
})

COPULAR_VERBS = frozenset({"be", "seem", "appear", "look", "happen", "turn"})


CLAUSAL_DEPS = frozenset({"xcomp", "ccomp", "advcl", "csubj", "acl"})


# ---------------------------------------------------------------------------
# Capa 1 - evidencia PERSONAL
# ---------------------------------------------------------------------------

# Pronombres personales referenciales en función de sujeto.
# reglas impersonales o, si nada dispara, la capa 2.
PERSONAL_PRONOUNS = frozenset({"i", "you", "he", "she", "we", "they"})

# Sujetos cuya referencialidad es dudosa a nivel de reglas: no cuentan
# como evidencia personal NI impersonal por sí mismos. Si además ninguna
# regla impersonal dispara, la oración cae como caso límite -> capa 2.
#   - it / there : posibles expletivos ("It is fast" puede ser referencial)
#   - one        : genérico/impersonal ("One must be careful")
AMBIGUOUS_SUBJECTS = frozenset({"it", "there", "one"})
