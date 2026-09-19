from models.issue import Issue
from models.verb_classification_type import VerbClassificationType
from models.error_code import ErrorCode
from rules.base_rule import Rule
from helpers.temporal_adverbials_helper import INCOMPATIBLE_TENSES

class TemporalAdverbRule(Rule):

    ERROR_CODE = ErrorCode.TEMPORAL_ADVERB_MISMATCH


    def evaluate(self, context) -> None:
        features_by_token = {}

        for verbFeature in context.verb_features:
            features_by_token[verbFeature.token.i] = verbFeature

        for adverb in context.advberbs:
            verb = self._find_governing_verb(adverb.root)
            if verb is None:
                continue

            features = features_by_token.get(verb.i)

            if features is None:
                continue

            adverb_text = adverb.text.lower()

            incompatible_tenses = INCOMPATIBLE_TENSES.get(
                adverb_text
            )

            if incompatible_tenses is None:
                continue

            tense_name = self._get_full_tense(features)

            if tense_name is None:
                continue

            if tense_name in incompatible_tenses:
                context.issues.append(
                    Issue(
                        fragment=f"{verb.text} {adverb.text}",
                        position=adverb.start_char,
                        explanation=(
                            f"Temporal adverb '{adverb.text}' is "
                            f"incompatible with {tense_name.lower().replace('_', ' ')}."
                        ),
                        error_code=self.ERROR_CODE,
                    )
                )

    @staticmethod
    def _find_governing_verb(token):
        current = token

        while current.head != current:
            current = current.head

            if current.pos_ in ("VERB", "AUX"):
                return current

        return None

    @staticmethod
    def _get_full_tense(features):

        tense = None
        aspects = set()

        for classification in features.classifications:

            if classification.classification_type == VerbClassificationType.TENSE:
                tense = classification.value

            elif classification.classification_type == VerbClassificationType.ASPECT:
                aspects.add(classification.value)

        if tense is None:
            return None

        # =========================================================
        # SIMPLE
        # =========================================================

        if aspects == {"SIMPLE"}:

            if tense == "PRESENT":
                return "PRESENT_SIMPLE"

            if tense == "PAST":
                return "PAST_SIMPLE"

            if tense == "FUTURE":
                return "FUTURE_SIMPLE"

        # =========================================================
        # CONTINUOUS
        # =========================================================

        if aspects == {"CONTINUOUS"}:

            if tense == "PRESENT":
                return "PRESENT_CONTINUOUS"

            if tense == "PAST":
                return "PAST_CONTINUOUS"

            if tense == "FUTURE":
                return "FUTURE_CONTINUOUS"

        # =========================================================
        # PERFECT
        # =========================================================

        if aspects == {"PERFECT"}:

            if tense == "PRESENT":
                return "PRESENT_PERFECT"

            if tense == "PAST":
                return "PAST_PERFECT"

            if tense == "FUTURE":
                return "FUTURE_PERFECT"

        # =========================================================
        # PERFECT CONTINUOUS
        # =========================================================

        if aspects == {"PERFECT", "CONTINUOUS"}:

            if tense == "PRESENT":
                return "PRESENT_PERFECT_CONTINUOUS"

            if tense == "PAST":
                return "PAST_PERFECT_CONTINUOUS"

            if tense == "FUTURE":
                return "FUTURE_PERFECT_CONTINUOUS"

        return None