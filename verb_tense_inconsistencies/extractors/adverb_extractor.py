import re

from helpers.temporal_adverbials_helper import (
    FUTURE_ADBS,
    PAST_ADBS,
    TEMPORAL_ADBS,
    TEMPORAL_COMP_ADVBS,
)


class AdverbExtractor:

    @staticmethod
    def extract(context):
        for token in context.sentence.doc:
            if token.text.lower() in (
                TEMPORAL_ADBS + FUTURE_ADBS + PAST_ADBS
            ):
                context.advberbs.append(
                    context.sentence.doc[
                        token.i - context.sentence.doc.start
                        : token.i - context.sentence.doc.start + 1
                    ]
                )

        for expression in TEMPORAL_COMP_ADVBS:
            pattern = rf"\b{re.escape(expression)}\b"
            for match in re.finditer(
                pattern,
                context.sentence.text,
                re.IGNORECASE,
            ):
                span = context.sentence.doc.char_span(
                    match.start(),
                    match.end(),
                )
                if span is not None:
                    context.advberbs.append(span)
