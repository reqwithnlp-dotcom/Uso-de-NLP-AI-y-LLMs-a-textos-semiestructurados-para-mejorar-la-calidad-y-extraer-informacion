import spacy

from extractors.verb_features_extractor import VerbFeaturesExtractor
from classifiers.verb_tense_classifier import VerbTenseClassifier
from models.verb_classification import VerbClassification


nlp = spacy.load("en_core_web_sm")


def get_verb(sentence, text):

    doc = nlp(sentence)

    return next(
        token
        for token in doc
        if token.text == text
    )


def classify(sentence, verb_text):

    token = get_verb(sentence, verb_text)

    features = VerbFeaturesExtractor.extract(token)

    return VerbTenseClassifier.classify(features)


def test_present_simple():

    result = classify(
        "The system validates the request.",
        "validates"
    )

    assert result == {
        VerbClassification.PRESENT,
        VerbClassification.SIMPLE
    }


def test_present_simple_negative():

    result = classify(
        "The system does not validate the request.",
        "validate"
    )

    assert result == {
        VerbClassification.PRESENT,
        VerbClassification.SIMPLE
    }


def test_present_perfect():

    result = classify(
        "The system has validated the request.",
        "validated"
    )

    assert result == {
        VerbClassification.PRESENT,
        VerbClassification.PERFECT
    }


def test_present_perfect_continuous():

    result = classify(
        "The system has been validating the request.",
        "validating"
    )

    assert result == {
        VerbClassification.PRESENT,
        VerbClassification.PERFECT,
        VerbClassification.CONTINUOUS
    }


def test_past_simple():

    result = classify(
        "The system validated the request.",
        "validated"
    )

    assert result == {
        VerbClassification.PAST,
        VerbClassification.SIMPLE
    }


def test_past_simple_negative():

    result = classify(
        "The system did not validate the request.",
        "validate"
    )

    assert result == {
        VerbClassification.PAST,
        VerbClassification.SIMPLE
    }


def test_past_perfect():

    result = classify(
        "The system had validated the request.",
        "validated"
    )

    assert result == {
        VerbClassification.PAST,
        VerbClassification.PERFECT
    }


def test_present_continuous():

    result = classify(
        "The system is validating the request.",
        "validating"
    )

    assert result == {
        VerbClassification.PRESENT,
        VerbClassification.CONTINUOUS
    }


def test_invalid_structure():

    result = classify(
        "The system has validate the request.",
        "validate"
    )

    assert result == set()


def test_past_continuous():

    result = classify(
        "The system was validating the request.",
        "validating"
    )

    assert result == {
        VerbClassification.PAST,
        VerbClassification.CONTINUOUS
    }


def test_past_perfect_continuous():

    result = classify(
        "The system had been validating the request.",
        "validating"
    )

    assert result == {
        VerbClassification.PAST,
        VerbClassification.PERFECT,
        VerbClassification.CONTINUOUS
    }


def test_future_simple():

    result = classify(
        "The system will validate the request.",
        "validate"
    )

    assert result == {
        VerbClassification.FUTURE,
        VerbClassification.SIMPLE
    }


def test_future_simple_negative():

    result = classify(
        "The system will not validate the request.",
        "validate"
    )

    assert result == {
        VerbClassification.FUTURE,
        VerbClassification.SIMPLE
    }


def test_future_continuous():

    result = classify(
        "The system will be validating the request.",
        "validating"
    )

    assert result == {
        VerbClassification.FUTURE,
        VerbClassification.CONTINUOUS
    }


def test_future_perfect():

    result = classify(
        "The system will have validated the request.",
        "validated"
    )

    assert result == {
        VerbClassification.FUTURE,
        VerbClassification.PERFECT
    }


def test_future_perfect_continuous():

    result = classify(
        "The system will have been validating the request.",
        "validating"
    )

    assert result == {
        VerbClassification.FUTURE,
        VerbClassification.PERFECT,
        VerbClassification.CONTINUOUS
    }