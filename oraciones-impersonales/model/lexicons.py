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



PERSONAL_PRONOUNS = frozenset({"i", "you", "he", "she", "we", "they"})


AMBIGUOUS_SUBJECTS = frozenset({"it", "there", "one"})
