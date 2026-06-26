import contractions


class TextNormalizer:

    @staticmethod
    def normalize(text: str) -> str:
        return contractions.fix(text)