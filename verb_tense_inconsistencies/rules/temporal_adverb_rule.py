from analyzer.analysis_context import AnalysisContext
from models.issue import Issue
from rules.base_rule import Rule
from models.error_code import ErrorCode
from helpers.time_by_adverb_rules import VERBS_ALLOW_PCONT
from spacy.tokens import Token

class TemporalAdverbRule(Rule):
    """
    Detects inconsistencies between temporal adverbs and verb tenses.

    Examples:
        The system validates the request yesterday.
        The system validated the request tomorrow.
    """


    """
    CLASS ANALYSIS CONTEXT:

    sentence: Span

    verb_phrases: list[VerbPhrase] = field(default_factory=list)

    issues: list[Issue] = field(default_factory=list)
    """

    """
    CLASS ISSUE:
    Represents a detected verb tense inconsistency.
        
    fragment: str
    position: int
    explanation: str
    error_code: str
    """

    """
    CLASS VERB_PHRASE:

    token: Token

    auxiliaries: list[str]

    verb_tag: str    

    tense: str | None
    """


    ERROR_CODE = ErrorCode.TEMPORAL_ADVERB_MISMATCH

    PAST_MARKERS = {
        "yesterday",
        "previous",
        "last",
        "former",
        "past",
        "preceding",
        "prior"
    }

    FUTURE_MARKERS = {
        "tomorrow",
        "next",
        "following",
        "upcoming",
        "coming",
        "future",
        "subsequent"
    }

    def simpleEvaluation(self, context: AnalysisContext) -> None:
        test_names = [
            "fut_advb_test",
            "past_advb_test",
            "since_test",
            "now_test",
            "by_test",
            "for_duration_test",
            "yet_test",
            "while_test",
            "when_test",
            "at_present_test",
        ]
        advb_words_to_tests = {test: False for test in test_names}


    def evaluate_adverb(adverb_token: Token, context: AnalysisContext, incompatible_tenses: list[str]) -> str:

        current = adverb_token

        # 1. Subir por el árbol de dependencias
        #    hasta encontrar un verbo.
        while current.head != current:

            current = current.head

            if current.pos_ in {"VERB", "AUX"}:
                break

        # No encontramos ningún verbo
        else:
            return "ERROR"

        # 2. Buscar el VerbPhrase correspondiente
        #    mediante la posición del token.
        for verb_phrase in context.verb_phrases:

            if verb_phrase.token.i == current.i:

                tense = verb_phrase.tense

                # 3. Comprobar compatibilidad
                if tense in incompatible_tenses:
                    return "ERROR"

                return "OK"

        # Encontramos el verbo, pero no existe
        # su VerbPhrase correspondiente.
        return "ERROR"

        