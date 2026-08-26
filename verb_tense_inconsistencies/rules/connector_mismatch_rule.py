from analyzer.analysis_context import AnalysisContext
from models.issue import Issue
from rules.base_rule import Rule
from models.error_code import ErrorCode
from models.verb_classification import VerbClassification


class ConnectorMismatchRule(Rule):
    """
    Detects tense inconsistencies between two verb structures
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

        if len(context.verb_features) < 2:
            return

        for token in sentence.doc:

            if token.text.lower() not in self.CONNECTORS:
                continue

            left = self._find_left_features(token.i, context)
            right = self._find_right_features(token.i, context)

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

    def _find_left_features(self, connector_index, context):

        candidates = [
            features
            for features in context.verb_features
            if features.token.i < connector_index
        ]

        if not candidates:
            return None

        return candidates[-1]

    def _find_right_features(self, connector_index, context):

        candidates = [
            features
            for features in context.verb_features
            if features.token.i > connector_index
        ]

        if not candidates:
            return None

        return candidates[0]

    @staticmethod
    def _is_mismatch(left, right):

        left_tense = ConnectorMismatchRule._get_tense(left)
        right_tense = ConnectorMismatchRule._get_tense(right)

        if left_tense is None or right_tense is None:
            return False

        return left_tense != right_tense

    @staticmethod
    def _get_tense(features):

        for classification in (
            VerbClassification.PRESENT,
            VerbClassification.PAST,
            VerbClassification.FUTURE,
        ):
            if features.has_classification(classification):
                return classification

        return None