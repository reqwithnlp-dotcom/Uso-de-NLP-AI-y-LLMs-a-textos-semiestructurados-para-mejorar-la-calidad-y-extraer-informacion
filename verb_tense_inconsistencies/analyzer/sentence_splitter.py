import spacy

from models.sentence_fragment import SentenceFragment


class SentenceSplitter:

    _nlp = spacy.load("en_core_web_sm")

    @classmethod
    def split(cls, text: str) -> list[SentenceFragment]:

        doc = cls._nlp(text)

        fragments = []

        for sent in doc.sents:

            fragments.append(
                SentenceFragment(
                    text=sent.text.strip(),
                    start_char=sent.start_char,
                    end_char=sent.end_char
                )
            )

        return fragments