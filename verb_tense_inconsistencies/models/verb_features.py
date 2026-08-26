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

    def has_classification(self, classification):
        return classification in self.classifications