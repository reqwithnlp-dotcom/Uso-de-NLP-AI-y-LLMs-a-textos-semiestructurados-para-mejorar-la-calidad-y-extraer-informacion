from analyzer.analysis_context import AnalysisContext
from models.issue import Issue
from rules.base_rule import Rule
from models.error_code import ErrorCode


class ConnectorMismatchRule(Rule):
    """
    Detects tense inconsistencies between two verb phrases
    connected by temporal or sequential connectors.

    Example:
        The user submits the request and the system responded.
    """

    ERROR_CODE = ErrorCode.CONNECTOR_MISMATCH

    CONNECTORS = {
        "and",
        "then",
        "after"
    }

    def evaluate(self, context: AnalysisContext) -> None:

        sentence = context.sentence

        if len(context.verb_phrases) < 2:
            return

        for token in sentence.doc:

            if token.text.lower() not in self.CONNECTORS:
                continue

            left = self._find_left_phrase(token.i, context)
            right = self._find_right_phrase(token.i, context)

            if left is None or right is None:
                continue

            if self._is_mismatch(left, right):

                context.issues.append(
                    Issue(
                        fragment=f"{left.token.text} {token.text} {right.token.text}",
                        position=token.idx,
                        explanation="Connected verb phrases use inconsistent tenses.",
                        error_code=self.ERROR_CODE
                    )
                )

    def _find_left_phrase(self, connector_index, context):

        candidates = [
            phrase
            for phrase in context.verb_phrases
            if phrase.token.i < connector_index
        ]

        if not candidates:
            return None

        return candidates[-1]

    def _find_right_phrase(self, connector_index, context):

        candidates = [
            phrase
            for phrase in context.verb_phrases
            if phrase.token.i > connector_index
        ]

        if not candidates:
            return None

        return candidates[0]

    @staticmethod
    def _is_mismatch(left, right):

        if left.tense is None or right.tense is None:
            return False

        left_family = left.tense.split("-")[-1]
        right_family = right.tense.split("-")[-1]

        return left_family != right_family