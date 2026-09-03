from analyzer.analysis_context import AnalysisContext
from models.issue import Issue
from models.error_code import ErrorCode
from models.verb_classification_type import VerbClassificationType
from rules.base_rule import Rule


class AuxiliaryMismatchRule(Rule):
    ERROR_CODE = ErrorCode.AUXILIARY_MISMATCH

    def evaluate(self, context: AnalysisContext) -> None:

        for features in context.verb_features:

            if not features.auxiliaries:
                continue

            if features.passive:
                continue

            has_tense = features.has_classification(
                VerbClassificationType.TENSE
            )

            has_valid_form = features.has_classification(
                VerbClassificationType.FORM,
                "VALID"
            )

            if not has_tense or not has_valid_form:
                self._add_issue(context, features)

    def _add_issue(self, context, features):

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

        words = [
            auxiliary.text
            for auxiliary in features.auxiliaries
        ]

        words.append(features.token.text)

        return " ".join(words)