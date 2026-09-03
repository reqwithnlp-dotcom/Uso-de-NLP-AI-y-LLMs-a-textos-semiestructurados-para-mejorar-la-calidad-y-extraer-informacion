class VerbFeatures:

    def __init__(
        self,
        token,
        auxiliaries=None,
        passive=False,
        negated=False,
        infinitive=False,
    ):
        self.token = token
        self.verb_tag = token.tag_
        self.auxiliaries = auxiliaries or []
        self.passive = passive
        self.negated = negated
        self.infinitive = infinitive

        self.classifications = set()

    def add_classification(self, classification):
        self.classifications.add(classification)

    def has_classification(
        self,
        classification_type,
        value=None
    ):
        return any(
            classification.classification_type == classification_type
            and (
                value is None
                or classification.value == value
            )
            for classification in self.classifications
        )