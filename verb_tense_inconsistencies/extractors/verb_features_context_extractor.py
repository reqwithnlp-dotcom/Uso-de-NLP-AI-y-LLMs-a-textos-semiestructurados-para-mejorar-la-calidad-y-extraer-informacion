from extractors.verb_features_extractor import VerbFeaturesExtractor


class VerbFeaturesContextExtractor:

    @staticmethod
    def extract(context):

        for token in context.sentence.doc:

            if token.pos_ == "VERB":
                features = VerbFeaturesExtractor.extract(token)
                context.verb_features.append(features)
                continue

            if VerbFeaturesContextExtractor._is_auxiliary_verb_candidate(token):
                features = VerbFeaturesExtractor.extract(token)
                context.verb_features.append(features)

    @staticmethod
    def _is_auxiliary_verb_candidate(token):

        return any(
            child.pos_ == "AUX"
            and child.dep_ in ("aux", "auxpass")
            for child in token.children
        )