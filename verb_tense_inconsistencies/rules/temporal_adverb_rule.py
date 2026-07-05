from analyzer.analysis_context import AnalysisContext
from models.issue import Issue
from rules.base_rule import Rule
from models.error_code import ErrorCode


class TemporalAdverbRule(Rule):
    """
    Detects inconsistencies between temporal adverbs and verb tenses.

    Examples:
        The system validates the request yesterday.
        The system validated the request tomorrow.
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

    def evaluate(self, context: AnalysisContext) -> None:

        sentence = context.sentence

        for token in sentence.doc:

            word = token.text.lower()

            if word in self.PAST_MARKERS:

                self._validate_marker(
                    token,
                    expected="past",
                    context=context
                )

            elif word in self.FUTURE_MARKERS:

                self._validate_marker(
                    token,
                    expected="fut",
                    context=context
                )

    def _validate_marker(
        self,
        marker_token,
        expected: str,
        context: AnalysisContext
    ) -> None:

        verb_phrase = self._find_related_verb(marker_token, context)

        if verb_phrase is None:
            return

        if verb_phrase.tense is None:
            return

        detected = verb_phrase.tense.split("-")[-1]

        if detected == expected:
            return

        context.issues.append(
            Issue(
                fragment=f"{marker_token.text} → {verb_phrase.token.text}",
                position=marker_token.idx,
                explanation=(
                    f"Temporal reference '{marker_token.text}' "
                    f"is inconsistent with the verb tense."
                ),
                error_code=self.ERROR_CODE
            )
        )

    @staticmethod
    def _find_related_verb(marker_token, context):

        head = marker_token.head

        while head != head.head:

            if head.pos_ == "VERB":
                break

            head = head.head

        if head.pos_ != "VERB":
            return None

        for phrase in context.verb_phrases:

            if phrase.token == head:
                return phrase

        return None