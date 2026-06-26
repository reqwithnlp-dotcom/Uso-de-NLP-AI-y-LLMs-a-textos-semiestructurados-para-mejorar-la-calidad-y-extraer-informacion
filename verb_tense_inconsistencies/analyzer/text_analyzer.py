from analyzer.normalizer import TextNormalizer
from analyzer.sentence_splitter import SentenceSplitter


class TextAnalyzer:

    def analyze(self, text: str):

        normalized_text = TextNormalizer.normalize(text)

        fragments = SentenceSplitter.split(normalized_text)

        return {
            "normalized_text": normalized_text,
            "fragments": fragments,
            "issues": []
        }