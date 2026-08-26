from models.verb_classification import VerbClassification


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
                VerbClassification.PRESENT,
                VerbClassification.SIMPLE
            }

        # Simple Past
        if not auxiliaries and verb_tag == "VBD":
            return {
                VerbClassification.PAST,
                VerbClassification.SIMPLE
            }

        # Present Simple with do/does
        if auxiliaries in (["do"], ["does"]) and verb_tag == "VB":
            return {
                VerbClassification.PRESENT,
                VerbClassification.SIMPLE
            }

        # Past Simple with did
        if auxiliaries == ["did"] and verb_tag == "VB":
            return {
                VerbClassification.PAST,
                VerbClassification.SIMPLE
            }

        # Present Perfect
        if auxiliaries in (["has"], ["have"]) and verb_tag == "VBN":
            return {
                VerbClassification.PRESENT,
                VerbClassification.PERFECT
            }

        # Past Perfect
        if auxiliaries == ["had"] and verb_tag == "VBN":
            return {
                VerbClassification.PAST,
                VerbClassification.PERFECT
            }

        # Present Continuous
        if auxiliaries in (["am"], ["is"], ["are"]) and verb_tag == "VBG":
            return {
                VerbClassification.PRESENT,
                VerbClassification.CONTINUOUS
            }

        # Past Continuous
        if auxiliaries in (["was"], ["were"]) and verb_tag == "VBG":
            return {
                VerbClassification.PAST,
                VerbClassification.CONTINUOUS
            }

        # Present Perfect Continuous
        if (
            auxiliaries in (["has", "been"], ["have", "been"])
            and verb_tag == "VBG"
        ):
            return {
                VerbClassification.PRESENT,
                VerbClassification.PERFECT,
                VerbClassification.CONTINUOUS
            }

        # Past Perfect Continuous
        if auxiliaries == ["had", "been"] and verb_tag == "VBG":
            return {
                VerbClassification.PAST,
                VerbClassification.PERFECT,
                VerbClassification.CONTINUOUS
            }

        # Future Simple
        if auxiliaries == ["will"] and verb_tag == "VB":
            return {
                VerbClassification.FUTURE,
                VerbClassification.SIMPLE
            }

        # Future Continuous
        if auxiliaries == ["will", "be"] and verb_tag == "VBG":
            return {
                VerbClassification.FUTURE,
                VerbClassification.CONTINUOUS
            }

        # Future Perfect
        if auxiliaries == ["will", "have"] and verb_tag == "VBN":
            return {
                VerbClassification.FUTURE,
                VerbClassification.PERFECT
            }

        # Future Perfect Continuous
        if (
            auxiliaries == ["will", "have", "been"]
            and verb_tag == "VBG"
        ):
            return {
                VerbClassification.FUTURE,
                VerbClassification.PERFECT,
                VerbClassification.CONTINUOUS
            }

        return set()

    @classmethod
    def classify_and_apply(cls, features):

        classifications = cls.classify(features)

        for classification in classifications:
            features.add_classification(classification)