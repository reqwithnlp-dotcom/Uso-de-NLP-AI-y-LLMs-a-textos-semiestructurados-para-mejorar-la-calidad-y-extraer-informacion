from helpers.verb_tense_rules import TEMP_VERB_RULES
from models.verb_phrase import VerbPhrase


class VerbTenseExtractor:

    @staticmethod
    def extract(context):

        aux = []

        for token in context.sentence.doc:

            if token.text.lower() == "not":
                continue

            if token.pos_ == "AUX":
                aux.append(token.text.lower())

            elif token.pos_ == "VERB":

                key = tuple(aux + [token.tag_])

                tense = TEMP_VERB_RULES.get(key)

                context.verb_phrases.append(

                    VerbPhrase(
                        token=token,
                        auxiliaries=aux.copy(),
                        verb_tag=token.tag_,
                        tense=tense
                    )
                )

                aux.clear()