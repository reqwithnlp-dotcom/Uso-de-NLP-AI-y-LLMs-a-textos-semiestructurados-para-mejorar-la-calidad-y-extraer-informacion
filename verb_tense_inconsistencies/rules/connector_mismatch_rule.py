from analyzer.analysis_context import AnalysisContext
from models.issue import Issue
from models.error_code import ErrorCode
from rules.base_rule import Rule
from models.verb_classification_type import VerbClassificationType


class ConnectorMismatchRule(Rule):
    """
    Detects tense inconsistencies between coordinated verb structures.

    Initial scope:
        and
        or
        but
        nor
        yet

    Temporal/subordinate connectors such as after, before, when,
    while or because are intentionally excluded because they may
    legitimately connect different verb tenses.
    """

    ERROR_CODE = ErrorCode.CONNECTOR_MISMATCH

    CONNECTORS = {
        "and",
        "or",
        "but",
        "nor",
        "yet",
    }

    def evaluate(self, context: AnalysisContext) -> None:

        if len(context.verb_features) < 2:
            return

        features_by_token = {
            features.token.i: features
            for features in context.verb_features
        }

        for right in context.verb_features:

            #
            # In a coordinated structure spaCy marks the second
            # verb as "conj" and points its head to the verb it
            # is coordinated with.
            #
            if right.token.dep_ != "conj":
                continue

            left = features_by_token.get(right.token.head.i)

            if left is None:
                continue

            connector = self._find_connector(
                left.token,
                right.token,
                context
            )

            if connector is None:
                continue

            if not self._is_mismatch(left, right):
                continue

            context.issues.append(
                Issue(
                    fragment=(
                        f"{left.token.text} "
                        f"{connector.text} "
                        f"{right.token.text}"
                    ),
                    position=connector.idx,
                    explanation=(
                        "Coordinated verb phrases use "
                        "inconsistent verb tenses."
                    ),
                    error_code=self.ERROR_CODE
                )
            )

    def _find_connector(self, left_token, right_token, context):

        start = min(left_token.i, right_token.i)
        end = max(left_token.i, right_token.i)

        candidates = [
            token
            for token in context.sentence.doc
            if start < token.i < end
            and token.text.lower() in self.CONNECTORS
        ]

        if not candidates:
            return None

        return candidates[-1]

    @staticmethod
    def _is_mismatch(left, right):

        left_tense = ConnectorMismatchRule._get_tense(left)
        right_tense = ConnectorMismatchRule._get_tense(right)

        if left_tense is None or right_tense is None:
            return False

        return left_tense != right_tense

    @staticmethod
    def _get_tense(features):

        for classification in features.classifications:

            if (
                classification.classification_type
                == VerbClassificationType.TENSE
            ):
                return classification.value

        return None