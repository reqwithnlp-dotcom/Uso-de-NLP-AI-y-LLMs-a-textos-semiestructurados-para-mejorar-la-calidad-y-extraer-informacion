from analyzer.analysis_context import AnalysisContext
from models.issue import Issue
from rules.base_rule import Rule
from models.error_code import ErrorCode
from verb_tense_inconsistencies.helpers.temporal_adverbials import VERBS_ALLOW_PCONT
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

   

    def simpleEvaluation(self, context: AnalysisContext) -> None:
        
        for adv in context.advberbs:
            if adv.text == "yet":
                self.evaluate_adverb(adv[0],context,["simp_pres","cont_pres","cont_past","cont_fut","cont_perf_fut"],)
            elif adv.text == "since":
                self.evaluate_adverb(adv[0],context,["cont_perf_fut","cont_fut","simp_fut"])
            elif adv.text == "now":
                self.evaluate_adverb(adv[0],context,["perf-past","cont_perf_past","perf_fut","cont_perf_fut"])
            elif adv.text == "by":
                self.evaluate_adverb(adv[0],context,["simp_pres","cont_pres","cont_past","cont_fut","cont_perf_fut"])
            elif adv[0] == "for": #AJUSTAR EL FOR PORQUE ES CONTEXTUAL
                self.evaluate_adverb(adv[0],context,[])
            elif adv.text == "while":
                self.evaluate_adverb(adv[0],context,[])
            elif adv.text == "when":
                self.evaluate_adverb(adv[0],context,[])                                                                                                                
            elif adv.text == "at present":
                self.evaluate_adverb(adv[0],context,["cont_perf_fut","perf_fut","cont_fut","simp_fut","cont_perf_past","perf-past","cont_past","simp_past"])
                                 

    def evaluate_adverb(adv,context: AnalysisContext, incompatible_tenses: list[str]) -> str:

        errors = []
        current = adv
        # 1. Subir por el árbol de dependencias
        #    hasta encontrar un verbo.
        while current.head != current:

            current = current.head

            if current.pos_ == "VERB":
                break
            # No encontramos ningún verbo
            else:
                errors.append ("ERROR: NO VERB WAS FOUND")

        # 2. Buscar el VerbPhrase correspondiente
        #    mediante la posición del token.
        for verb_phrase in context.verb_phrases:

            if verb_phrase.token.i == current.i:

                tense = verb_phrase.tense

                # 3. Comprobar compatibilidad
                if tense in incompatible_tenses:
                    errors.append(f"error with {adv.text} and {tense}")