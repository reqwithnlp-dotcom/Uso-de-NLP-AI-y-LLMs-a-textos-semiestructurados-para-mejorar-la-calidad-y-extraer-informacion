import spacy

from models.sentence_fragment import SentenceFragment


nlp = spacy.load("en_core_web_md")


class SentenceSplitter:

    @staticmethod
    def split(text: str):

        text = text.strip()

        doc = nlp(text)

        fragments = []

        for sent in doc.sents:

            fragments.append(
                SentenceFragment(
                    text=sent.text.strip(),
                    doc=sent,
                    start_char=sent.start_char,
                    end_char=sent.end_char
                )
            )

        return fragments