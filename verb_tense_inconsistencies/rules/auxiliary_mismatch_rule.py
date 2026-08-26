from analyzer.analysis_context import AnalysisContext
from models.issue import Issue
from rules.base_rule import Rule
from models.error_code import ErrorCode


class AuxiliaryMismatchRule(Rule):
    """
    Detects invalid auxiliary verb sequences.

    If a verb phrase cannot be classified into a valid
    tense/aspect combination, its classifications set
    will be empty.
    """

    ERROR_CODE = ErrorCode.AUXILIARY_MISMATCH

    def evaluate(self, context: AnalysisContext) -> None:

        for features in context.verb_features:

            if features.classifications:
                continue

            context.issues.append(
                Issue(
                    fragment=self._build_fragment(features),
                    position=features.token.idx,
                    explanation="Invalid auxiliary verb sequence.",
                    error_code=self.ERROR_CODE
                )
            )

    @staticmethod
    def _build_fragment(features) -> str:
        """
        Builds a readable representation of the verb structure.

        Example:
            auxiliaries = [Token("has")]
            verb = processed

            -> "has processed"
        """

        words = [
            auxiliary.text
            for auxiliary in features.auxiliaries
        ]

        words.append(features.token.text)

        return " ".join(words)