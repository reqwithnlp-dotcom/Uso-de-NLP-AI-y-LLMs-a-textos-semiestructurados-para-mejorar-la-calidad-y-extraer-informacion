from extractors.verb_features_extractor import VerbFeaturesExtractor


class VerbFeaturesContextExtractor:

    @staticmethod
    def extract(context):

        for token in context.sentence.doc:

            if token.pos_ != "VERB":
                continue

            features = VerbFeaturesExtractor.extract(token)

            context.verb_features.append(features)