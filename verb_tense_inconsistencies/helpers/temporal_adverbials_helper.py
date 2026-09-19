TEMPORAL_ADBS = [
    "since",
    "now",
    "by",
    "yet",
    "while",
    "when",
    "one day",
    "for",
]
TEMPORAL_COMP_ADVBS = [
    "at present",
]

FUTURE_ADVERBS = [
    "tomorrow",
    "next",
    "soon",
    "later",
    "afterward",
    "afterwards",
    "eventually",
    "someday",
    "tonight",
    "upcoming",
    "forthcoming",
    "following",
    "subsequent",
    "future",
    "coming",
]

PAST_ADVERBS = [
    "yesterday",
    "last",
    "ago",
    "before",
    "previously",
    "earlier",
    "formerly",
    "recently",
    "once",
    "formerly",
    "back then",
    "in the past",
    "former",
    "past",
    "preceding",
    "prior"
]

PAST_INCOMPATIBLE_TENSES = {
    "PRESENT_SIMPLE",
    "PRESENT_CONTINUOUS",
    "PRESENT_PERFECT",
    "PRESENT_PERFECT_CONTINUOUS",
    "FUTURE_SIMPLE",
    "FUTURE_CONTINUOUS",
    "FUTURE_PERFECT",
    "FUTURE_PERFECT_CONTINUOUS",
}
FUTURE_INCOMPATIBLE_TENSES = {
    "PAST_SIMPLE",
    "PAST_CONTINUOUS",
    "PAST_PERFECT",
    "PAST_PERFECT_CONTINUOUS",
}


# 1. Agregamos todos los adverbios de pasado
INCOMPATIBLE_TENSES = {
    adverb: PAST_INCOMPATIBLE_TENSES
    for adverb in PAST_ADVERBS
}


# 2. Agregamos todos los adverbios de futuro
INCOMPATIBLE_TENSES.update({
    adverb: FUTURE_INCOMPATIBLE_TENSES
    for adverb in FUTURE_ADVERBS
})


INCOMPATIBLE_TENSES.update({

        # =========================================================
        # PRESENTE / MOMENTO ACTUAL
        # =========================================================

        "now": {
            "PAST_SIMPLE",
            "PAST_CONTINUOUS",
            "PAST_PERFECT",
            "PAST_PERFECT_CONTINUOUS",
        },

        "at present": {
            "PAST_SIMPLE",
            "PAST_CONTINUOUS",
            "PAST_PERFECT",
            "PAST_PERFECT_CONTINUOUS",
        },

        "currently": {
            "PAST_SIMPLE",
            "PAST_CONTINUOUS",
            "PAST_PERFECT",
            "PAST_PERFECT_CONTINUOUS",
        },

        "at the moment": {
            "PAST_SIMPLE",
            "PAST_CONTINUOUS",
            "PAST_PERFECT",
            "PAST_PERFECT_CONTINUOUS",
        },

        # =========================================================
        # RECIENTEMENTE
        # =========================================================

        "recently": set(),

        # =========================================================
        # ANTERIORMENTE / MÁS TEMPRANO
        # =========================================================

        "earlier": set(),

        # =========================================================
        # FUTURO CERCANO / POSTERIOR
        # =========================================================

        "soon": {
            "PAST_SIMPLE",
            "PAST_CONTINUOUS",
            "PAST_PERFECT",
            "PAST_PERFECT_CONTINUOUS",
        },

        "later": {
            "PAST_SIMPLE",
            "PAST_CONTINUOUS",
            "PAST_PERFECT",
            "PAST_PERFECT_CONTINUOUS",
        },

        "afterward": {
            "PAST_SIMPLE",
            "PAST_CONTINUOUS",
            "PAST_PERFECT",
            "PAST_PERFECT_CONTINUOUS",
        },

        "afterwards": {
            "PAST_SIMPLE",
            "PAST_CONTINUOUS",
            "PAST_PERFECT",
            "PAST_PERFECT_CONTINUOUS",
        },

        # =========================================================
        # SINCE
        # =========================================================

        "since": {
            "PRESENT_SIMPLE",
            "PRESENT_CONTINUOUS",
            "PAST_SIMPLE",
            "PAST_CONTINUOUS",
            "FUTURE_SIMPLE",
            "FUTURE_CONTINUOUS",
        },

        # =========================================================
        # YET
        # =========================================================

        "yet": {
            "PRESENT_SIMPLE",
            "PRESENT_CONTINUOUS",
        },

        # =========================================================
        # FOR
        # =========================================================

        "for": {
            "PRESENT_SIMPLE",
            "PRESENT_CONTINUOUS",
            "FUTURE_SIMPLE",
            "FUTURE_CONTINUOUS",
        },

        # =========================================================
        # BY
        # =========================================================

        "by": {
            "PAST_SIMPLE",
            "PAST_CONTINUOUS",
            "PAST_PERFECT",
            "PAST_PERFECT_CONTINUOUS",
        },
})
