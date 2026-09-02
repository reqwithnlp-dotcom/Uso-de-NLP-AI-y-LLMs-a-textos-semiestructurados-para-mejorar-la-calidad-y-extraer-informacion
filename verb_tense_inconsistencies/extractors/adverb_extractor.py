from models.verb_phrase import VerbPhrase
from helpers.temporal_adverbials import TEMPORAL_ADBS, FUTURE_ADBS, PAST_ADBS
import re
class AdverbExtractor:

    @staticmethod
    def extract(context):

        pattern = r"\b(?:for duration|at present)\b"

        temporal_expressions = []

        for match in re.finditer(pattern, context.sentence.text, re.IGNORECASE):
            start_char = match.start()
            end_char = match.end()

            span = context.sentence.char_span(start_char, end_char)

            if span is not None:
                temporal_expressions.append(span)
                
        for token in context.sentence:

            if  (
                token.text in TEMPORAL_ADBS or
                token.text in FUTURE_ADBS or
                token.text in PAST_ADBS
                ):
                context.adverbs.append(context.sentence[token.i : token.i + 1])
