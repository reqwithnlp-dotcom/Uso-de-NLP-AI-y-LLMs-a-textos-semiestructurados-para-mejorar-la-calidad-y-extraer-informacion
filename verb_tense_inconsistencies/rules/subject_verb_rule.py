from analyzer.analysis_context import AnalysisContext
from models.issue import Issue
from rules.base_rule import Rule
from models.error_code import ErrorCode


class SubjectVerbRule(Rule):
    """
    Detects subject-verb agreement inconsistencies.

    Current implementation handles the most common cases:
    - He/She/It + VBP
    - They/We/You + VBZ

    This rule can be extended later to support nouns,
    coordinated subjects and more complex agreement cases.
    """

    ERROR_CODE = ErrorCode.SUBJECT_VERB_MISMATCH

    THIRD_PERSON_SINGULAR = {
        "he",
        "she",
        "it"
    }

    NON_THIRD_PERSON = {
        "i",
        "you",
        "we",
        "they"
    }

    def evaluate(self, context: AnalysisContext) -> None:

        sentence = context.sentence

        subject = None
        root_verb = None

        for token in sentence.doc:

            if token.dep_ == "nsubj":
                subject = token

            elif token.dep_ == "ROOT" and token.pos_ == "VERB":
                root_verb = token

        if subject is None or root_verb is None:
            return

        subject_text = subject.text.lower()

        mismatch = False

        if (
            subject_text in self.THIRD_PERSON_SINGULAR
            and root_verb.tag_ == "VBP"
        ):
            mismatch = True

        elif (
            subject_text in self.NON_THIRD_PERSON
            and root_verb.tag_ == "VBZ"
        ):
            mismatch = True

        if not mismatch:
            return

        context.issues.append(
            Issue(
                fragment=f"{subject.text} {root_verb.text}",
                position=root_verb.idx,
                explanation="Subject and verb do not agree in number.",
                error_code=self.ERROR_CODE
            )
        )