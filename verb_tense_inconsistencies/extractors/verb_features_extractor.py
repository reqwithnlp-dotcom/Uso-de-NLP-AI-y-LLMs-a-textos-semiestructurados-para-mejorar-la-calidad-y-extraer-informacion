import token

from models.verb_features import VerbFeatures


class VerbFeaturesExtractor:

    @staticmethod
    def extract(token):

        auxiliaries = []
        passive = False
        negated = False
        infinitive = False

        for child in token.children:

            if child.text.lower() == "to":
                infinitive = True

            elif child.dep_ in ("aux", "auxpass"):

                auxiliaries.append(child)

                if child.dep_ == "auxpass":
                    passive = True

            elif child.dep_ == "neg":
                negated = True

        if (
            token.dep_ == "xcomp"
            and token.head.pos_ == "AUX"
        ):
            auxiliaries.append(token.head)
            
        return VerbFeatures(
            token=token,
            auxiliaries=auxiliaries,
            passive=passive,
            negated=negated,
            infinitive=infinitive,
        )