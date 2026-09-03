from models.verb_classification import VerbClassification
from models.verb_classification_type import VerbClassificationType


class VerbTenseClassifier:

    @staticmethod
    def classify(features):

        verb_tag = features.verb_tag

        auxiliaries = [
            aux.text.lower()
            for aux in features.auxiliaries
        ]

        # Simple Present
        if not auxiliaries and verb_tag in ("VBZ", "VBP"):
            return {
                VerbClassification(
                    VerbClassificationType.TENSE,
                    "PRESENT"
                ),
                VerbClassification(
                    VerbClassificationType.ASPECT,
                    "SIMPLE"
                )
            }

        # Simple Past
        if not auxiliaries and verb_tag == "VBD":
            return {
                VerbClassification(
                    VerbClassificationType.TENSE,
                    "PAST"
                ),
                VerbClassification(
                    VerbClassificationType.ASPECT,
                    "SIMPLE"
                )
            }

        # Present Simple with do/does
        if auxiliaries in (["do"], ["does"]) and verb_tag == "VB":
            return {
                VerbClassification(
                    VerbClassificationType.TENSE,
                    "PRESENT"
                ),
                VerbClassification(
                    VerbClassificationType.ASPECT,
                    "SIMPLE"
                )
            }

        # Past Simple with did
        if auxiliaries == ["did"] and verb_tag == "VB":
            return {
                VerbClassification(
                    VerbClassificationType.TENSE,
                    "PAST"
                ),
                VerbClassification(
                    VerbClassificationType.ASPECT,
                    "SIMPLE"
                )
            }

        # Present Perfect
        if auxiliaries in (["has"], ["have"]) and verb_tag == "VBN":
            return {
                VerbClassification(
                    VerbClassificationType.TENSE,
                    "PRESENT"
                ),
                VerbClassification(
                    VerbClassificationType.ASPECT,
                    "PERFECT"
                )
            }

        # Past Perfect
        if auxiliaries == ["had"] and verb_tag == "VBN":
            return {
                VerbClassification(
                    VerbClassificationType.TENSE,
                    "PAST"
                ),
                VerbClassification(
                    VerbClassificationType.ASPECT,
                    "PERFECT"
                )
            }

        # Present Continuous
        if auxiliaries in (["am"], ["is"], ["are"]) and verb_tag == "VBG":
            return {
                VerbClassification(
                    VerbClassificationType.TENSE,
                    "PRESENT"
                ),
                VerbClassification(
                    VerbClassificationType.ASPECT,
                    "CONTINUOUS"
                )
            }

        # Past Continuous
        if auxiliaries in (["was"], ["were"]) and verb_tag == "VBG":
            return {
                VerbClassification(
                    VerbClassificationType.TENSE,
                    "PAST"
                ),
                VerbClassification(
                    VerbClassificationType.ASPECT,
                    "CONTINUOUS"
                )
            }

        # Present Perfect Continuous
        if (
            auxiliaries in (["has", "been"], ["have", "been"])
            and verb_tag == "VBG"
        ):
            return {
                VerbClassification(
                    VerbClassificationType.TENSE,
                    "PRESENT"
                ),
                VerbClassification(
                    VerbClassificationType.ASPECT,
                    "PERFECT"
                ),
                VerbClassification(
                    VerbClassificationType.ASPECT,
                    "CONTINUOUS"
                )
            }

        # Past Perfect Continuous
        if auxiliaries == ["had", "been"] and verb_tag == "VBG":
            return {
                VerbClassification(
                    VerbClassificationType.TENSE,
                    "PAST"
                ),
                VerbClassification(
                    VerbClassificationType.ASPECT,
                    "PERFECT"
                ),
                VerbClassification(
                    VerbClassificationType.ASPECT,
                    "CONTINUOUS"
                )
            }

        # Future Simple
        if auxiliaries == ["will"] and verb_tag == "VB":
            return {
                VerbClassification(
                    VerbClassificationType.TENSE,
                    "FUTURE"
                ),
                VerbClassification(
                    VerbClassificationType.ASPECT,
                    "SIMPLE"
                )
            }

        # Future Continuous
        if auxiliaries == ["will", "be"] and verb_tag == "VBG":
            return {
                VerbClassification(
                    VerbClassificationType.TENSE,
                    "FUTURE"
                ),
                VerbClassification(
                    VerbClassificationType.ASPECT,
                    "CONTINUOUS"
                )
            }

        # Future Perfect
        if auxiliaries == ["will", "have"] and verb_tag == "VBN":
            return {
                VerbClassification(
                    VerbClassificationType.TENSE,
                    "FUTURE"
                ),
                VerbClassification(
                    VerbClassificationType.ASPECT,
                    "PERFECT"
                )
            }

        # Future Perfect Continuous
        if (
            auxiliaries == ["will", "have", "been"]
            and verb_tag == "VBG"
        ):
            return {
                VerbClassification(
                    VerbClassificationType.TENSE,
                    "FUTURE"
                ),
                VerbClassification(
                    VerbClassificationType.ASPECT,
                    "PERFECT"
                ),
                VerbClassification(
                    VerbClassificationType.ASPECT,
                    "CONTINUOUS"
                )
            }

        return set()

    @classmethod
    def classify_and_apply(cls, features):

        classifications = cls.classify(features)

        for classification in classifications:
            features.add_classification(classification)