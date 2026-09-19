from lemminflect import getInflection

from models.verb_classification import VerbClassification
from models.verb_classification_type import VerbClassificationType


class VerbFormClassifier:

    @classmethod
    def classify_and_apply(cls, features):

        if cls.is_valid_form(
            word=features.token.text,
            lemma=features.token.lemma_,
            expected_tag=features.verb_tag
        ):
            features.add_classification(
                VerbClassification(
                    VerbClassificationType.FORM,
                    "VALID"
                )
            )

    @classmethod
    def is_valid_form(
        cls,
        word: str,
        lemma: str,
        expected_tag: str
    ) -> bool:

        word = word.lower()
        lemma = lemma.lower()

        inflections = getInflection(
            lemma,
            tag=expected_tag
        )

        return word in {
            form.lower()
            for form in inflections
        }