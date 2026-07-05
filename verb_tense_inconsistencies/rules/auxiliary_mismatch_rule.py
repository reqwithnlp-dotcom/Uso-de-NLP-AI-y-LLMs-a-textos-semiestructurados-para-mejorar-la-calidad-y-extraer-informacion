from analyzer.analysis_context import AnalysisContext
from models.issue import Issue
from rules.base_rule import Rule
from models.error_code import ErrorCode


class AuxiliaryMismatchRule(Rule):
    """
    Detects invalid auxiliary verb sequences.

    The VerbTenseExtractor attempts to identify the tense of every verb phrase.
    If a verb phrase cannot be matched against the known auxiliary patterns,
    its tense will be None.
    """

    ERROR_CODE = ErrorCode.AUXILIARY_MISMATCH

    def evaluate(self, context: AnalysisContext) -> None:

        for phrase in context.verb_phrases:

            if phrase.tense is not None:
                continue

            context.issues.append(
                Issue(
                    fragment=self._build_fragment(phrase),
                    position=phrase.token.idx,
                    explanation="Invalid auxiliary verb sequence.",
                    error_code=self.ERROR_CODE
                )
            )

    @staticmethod
    def _build_fragment(phrase) -> str:
        """
        Builds a readable representation of the verb phrase.

        Example:
            auxiliaries = ["has"]
            verb = processed

            -> "has processed"
        """

        words = phrase.auxiliaries

        words.append(phrase.token.text)

        return " ".join(words)