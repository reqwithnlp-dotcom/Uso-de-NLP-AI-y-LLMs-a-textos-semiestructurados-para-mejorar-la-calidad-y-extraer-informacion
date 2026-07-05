from analyzer.analysis_context import AnalysisContext
from models.issue import Issue
from rules.base_rule import Rule
from models.error_code import ErrorCode


class TenseMismatchRule(Rule):
    """
    Detects the coexistence of present and past verb tenses
    within the same sentence.

    This is a simple heuristic intended to detect obvious
    inconsistencies in requirement specifications.

    More advanced temporal consistency rules will replace
    this rule in future versions.
    """

    ERROR_CODE = ErrorCode.TENSE_MISMATCH

    def evaluate(self, context: AnalysisContext) -> None:

        has_present = False
        has_past = False

        present_verbs = []
        past_verbs = []

        for phrase in context.verb_phrases:

            if phrase.tense is None:
                continue

            family = phrase.tense.split("-")[-1]

            if family == "pres":
                has_present = True
                present_verbs.append(phrase)

            elif family == "past":
                has_past = True
                past_verbs.append(phrase)

        if not (has_present and has_past):
            return

        context.issues.append(
            Issue(
                fragment=self._build_fragment(
                    present_verbs,
                    past_verbs
                ),
                position=min(
                    present_verbs[0].token.idx,
                    past_verbs[0].token.idx
                ),
                explanation=(
                    "The sentence contains both present and past "
                    "verb tenses."
                ),
                error_code=self.ERROR_CODE
            )
        )

    @staticmethod
    def _build_fragment(present_verbs, past_verbs):

        verbs = []

        verbs.extend(v.token.text for v in present_verbs)
        verbs.extend(v.token.text for v in past_verbs)

        return ", ".join(verbs)