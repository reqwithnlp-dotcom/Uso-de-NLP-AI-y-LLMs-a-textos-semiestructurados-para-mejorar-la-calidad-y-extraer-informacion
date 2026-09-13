import spacy

from extractors.verb_features_extractor import VerbFeaturesExtractor
from classifiers.verb_tense_classifier import VerbTenseClassifier
from models.verb_classification import VerbClassification
from models.verb_classification_type import VerbClassificationType


nlp = spacy.load("en_core_web_md")


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


def tense(value):
    return VerbClassification(
        VerbClassificationType.TENSE,
        value
    )


def aspect(value):
    return VerbClassification(
        VerbClassificationType.ASPECT,
        value
    )


def test_present_simple():

    result = classify(
        "The system validates the request.",
        "validates"
    )

    assert result == {
        tense("PRESENT"),
        aspect("SIMPLE")
    }


def test_present_simple_negative():

    result = classify(
        "The system does not validate the request.",
        "validate"
    )

    assert result == {
        tense("PRESENT"),
        aspect("SIMPLE")
    }


def test_present_perfect():

    result = classify(
        "The system has validated the request.",
        "validated"
    )

    assert result == {
        tense("PRESENT"),
        aspect("PERFECT")
    }


def test_present_perfect_continuous():

    result = classify(
        "The system has been validating the request.",
        "validating"
    )

    assert result == {
        tense("PRESENT"),
        aspect("PERFECT"),
        aspect("CONTINUOUS")
    }


def test_past_simple():

    result = classify(
        "The system validated the request.",
        "validated"
    )

    assert result == {
        tense("PAST"),
        aspect("SIMPLE")
    }


def test_past_simple_negative():

    result = classify(
        "The system did not validate the request.",
        "validate"
    )

    assert result == {
        tense("PAST"),
        aspect("SIMPLE")
    }


def test_past_perfect():

    result = classify(
        "The system had validated the request.",
        "validated"
    )

    assert result == {
        tense("PAST"),
        aspect("PERFECT")
    }


def test_present_continuous():

    result = classify(
        "The system is validating the request.",
        "validating"
    )

    assert result == {
        tense("PRESENT"),
        aspect("CONTINUOUS")
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
        tense("PAST"),
        aspect("CONTINUOUS")
    }


def test_past_perfect_continuous():

    result = classify(
        "The system had been validating the request.",
        "validating"
    )

    assert result == {
        tense("PAST"),
        aspect("PERFECT"),
        aspect("CONTINUOUS")
    }


def test_future_simple():

    result = classify(
        "The system will validate the request.",
        "validate"
    )

    assert result == {
        tense("FUTURE"),
        aspect("SIMPLE")
    }


def test_future_simple_negative():

    result = classify(
        "The system will not validate the request.",
        "validate"
    )

    assert result == {
        tense("FUTURE"),
        aspect("SIMPLE")
    }


def test_future_continuous():

    result = classify(
        "The system will be validating the request.",
        "validating"
    )

    assert result == {
        tense("FUTURE"),
        aspect("CONTINUOUS")
    }


def test_future_perfect():

    result = classify(
        "The system will have validated the request.",
        "validated"
    )

    assert result == {
        tense("FUTURE"),
        aspect("PERFECT")
    }


def test_future_perfect_continuous():

    result = classify(
        "The system will have been validating the request.",
        "validating"
    )

    assert result == {
        tense("FUTURE"),
        aspect("PERFECT"),
        aspect("CONTINUOUS")
    }

def test_present_simple_with_infinitive():

    doc = nlp(
        "The system needs to validate the request."
    )

    needs_token = next(
        token
        for token in doc
        if token.text == "needs"
    )

    validate_token = next(
        token
        for token in doc
        if token.text == "validate"
    )

    needs_features = VerbFeaturesExtractor.extract(
        needs_token
    )

    validate_features = VerbFeaturesExtractor.extract(
        validate_token
    )

    needs_result = VerbTenseClassifier.classify(
        needs_features
    )

    validate_result = VerbTenseClassifier.classify(
        validate_features
    )

    assert needs_result == {
        tense("PRESENT"),
        aspect("SIMPLE")
    }

    assert validate_features.infinitive is True

    assert validate_result == set()

def test_present_simple_have_to_with_infinitive():

    doc = nlp(
        "The system has to validate the request."
    )

    has_token = next(
        token
        for token in doc
        if token.text == "has"
    )

    validate_token = next(
        token
        for token in doc
        if token.text == "validate"
    )

    has_features = VerbFeaturesExtractor.extract(
        has_token
    )

    validate_features = VerbFeaturesExtractor.extract(
        validate_token
    )

    has_result = VerbTenseClassifier.classify(
        has_features
    )

    validate_result = VerbTenseClassifier.classify(
        validate_features
    )

    assert has_result == {
        tense("PRESENT"),
        aspect("SIMPLE")
    }

    assert validate_features.infinitive is True

    assert validate_result == set()

def test_past_simple_have_to_with_infinitive():

    doc = nlp(
        "The system had to validate the request."
    )

    had_token = next(
        token
        for token in doc
        if token.text == "had"
    )

    validate_token = next(
        token
        for token in doc
        if token.text == "validate"
    )

    had_features = VerbFeaturesExtractor.extract(
        had_token
    )

    validate_features = VerbFeaturesExtractor.extract(
        validate_token
    )

    had_result = VerbTenseClassifier.classify(
        had_features
    )

    validate_result = VerbTenseClassifier.classify(
        validate_features
    )

    assert had_result == {
        tense("PAST"),
        aspect("SIMPLE")
    }

    assert validate_features.infinitive is True

    assert validate_result == set()

def test_future_simple_have_to_with_infinitive():

    doc = nlp(
        "The system will have to validate the request."
    )

    have_token = next(
        token
        for token in doc
        if token.text == "have"
    )

    validate_token = next(
        token
        for token in doc
        if token.text == "validate"
    )

    have_features = VerbFeaturesExtractor.extract(
        have_token
    )

    validate_features = VerbFeaturesExtractor.extract(
        validate_token
    )

    have_result = VerbTenseClassifier.classify(
        have_features
    )

    validate_result = VerbTenseClassifier.classify(
        validate_features
    )

    assert have_result == {
        tense("FUTURE"),
        aspect("SIMPLE")
    }

    assert validate_features.infinitive is True

    assert validate_result == set()

def test_present_perfect_with_infinitive():

    doc = nlp(
        "The system has needed to validate the request."
    )

    needed_token = next(
        token
        for token in doc
        if token.text == "needed"
    )

    validate_token = next(
        token
        for token in doc
        if token.text == "validate"
    )

    needed_features = VerbFeaturesExtractor.extract(
        needed_token
    )

    validate_features = VerbFeaturesExtractor.extract(
        validate_token
    )

    needed_result = VerbTenseClassifier.classify(
        needed_features
    )

    validate_result = VerbTenseClassifier.classify(
        validate_features
    )

    assert needed_result == {
        tense("PRESENT"),
        aspect("PERFECT")
    }

    assert validate_features.infinitive is True

    assert validate_result == set()

def test_future_simple_need_to_with_infinitive():

    doc = nlp(
        "The system will need to validate the request."
    )

    need_token = next(
        token
        for token in doc
        if token.text == "need"
    )

    validate_token = next(
        token
        for token in doc
        if token.text == "validate"
    )

    need_features = VerbFeaturesExtractor.extract(
        need_token
    )

    validate_features = VerbFeaturesExtractor.extract(
        validate_token
    )

    need_result = VerbTenseClassifier.classify(
        need_features
    )

    validate_result = VerbTenseClassifier.classify(
        validate_features
    )

    assert need_result == {
        tense("FUTURE"),
        aspect("SIMPLE")
    }

    assert validate_features.infinitive is True

    assert validate_result == set()

def test_present_simple_negative_need_to_with_infinitive():

    doc = nlp(
        "The system does not need to validate the request."
    )

    need_token = next(
        token
        for token in doc
        if token.text == "need"
    )

    validate_token = next(
        token
        for token in doc
        if token.text == "validate"
    )

    need_features = VerbFeaturesExtractor.extract(
        need_token
    )

    validate_features = VerbFeaturesExtractor.extract(
        validate_token
    )

    need_result = VerbTenseClassifier.classify(
        need_features
    )

    validate_result = VerbTenseClassifier.classify(
        validate_features
    )

    assert need_result == {
        tense("PRESENT"),
        aspect("SIMPLE")
    }

    assert need_features.negated is True

    assert validate_features.infinitive is True

    assert validate_result == set()

def test_present_simple_negative_have_to_with_infinitive():

    doc = nlp(
        "The system does not have to validate the request."
    )

    have_token = next(
        token
        for token in doc
        if token.text == "have"
    )

    validate_token = next(
        token
        for token in doc
        if token.text == "validate"
    )

    have_features = VerbFeaturesExtractor.extract(
        have_token
    )

    validate_features = VerbFeaturesExtractor.extract(
        validate_token
    )

    have_result = VerbTenseClassifier.classify(
        have_features
    )

    validate_result = VerbTenseClassifier.classify(
        validate_features
    )

    assert have_result == {
        tense("PRESENT"),
        aspect("SIMPLE")
    }

    assert have_features.negated is True

    assert validate_features.infinitive is True

    assert validate_result == set()

def test_present_simple_passive_with_infinitive():

    doc = nlp(
        "The system is required to validate the request."
    )

    required_token = next(
        token
        for token in doc
        if token.text == "required"
    )

    validate_token = next(
        token
        for token in doc
        if token.text == "validate"
    )

    required_features = VerbFeaturesExtractor.extract(
        required_token
    )

    validate_features = VerbFeaturesExtractor.extract(
        validate_token
    )

    required_result = VerbTenseClassifier.classify(
        required_features
    )

    validate_result = VerbTenseClassifier.classify(
        validate_features
    )

    assert required_features.passive is True

    assert required_result == {
        tense("PRESENT"),
        aspect("SIMPLE")
    }

    assert validate_features.infinitive is True

    assert validate_result == set()

def test_past_simple_passive_with_infinitive():

    doc = nlp(
        "The system was required to validate the request."
    )

    required_token = next(
        token
        for token in doc
        if token.text == "required"
    )

    validate_token = next(
        token
        for token in doc
        if token.text == "validate"
    )

    required_features = VerbFeaturesExtractor.extract(
        required_token
    )

    validate_features = VerbFeaturesExtractor.extract(
        validate_token
    )

    required_result = VerbTenseClassifier.classify(
        required_features
    )

    validate_result = VerbTenseClassifier.classify(
        validate_features
    )

    assert required_features.passive is True

    assert required_result == {
        tense("PAST"),
        aspect("SIMPLE")
    }

    assert validate_features.infinitive is True

    assert validate_result == set()

def test_future_simple_passive_with_infinitive():

    doc = nlp(
        "The system will be required to validate the request."
    )

    required_token = next(
        token
        for token in doc
        if token.text == "required"
    )

    validate_token = next(
        token
        for token in doc
        if token.text == "validate"
    )

    required_features = VerbFeaturesExtractor.extract(
        required_token
    )

    validate_features = VerbFeaturesExtractor.extract(
        validate_token
    )

    required_result = VerbTenseClassifier.classify(
        required_features
    )

    validate_result = VerbTenseClassifier.classify(
        validate_features
    )

    assert required_features.passive is True

    assert required_result == {
        tense("FUTURE"),
        aspect("SIMPLE")
    }

    assert validate_features.infinitive is True

    assert validate_result == set()

def test_present_perfect_passive_with_infinitive():

    doc = nlp(
        "The system has been required to validate the request."
    )

    required_token = next(
        token
        for token in doc
        if token.text == "required"
    )

    validate_token = next(
        token
        for token in doc
        if token.text == "validate"
    )

    required_features = VerbFeaturesExtractor.extract(
        required_token
    )

    validate_features = VerbFeaturesExtractor.extract(
        validate_token
    )

    required_result = VerbTenseClassifier.classify(
        required_features
    )

    validate_result = VerbTenseClassifier.classify(
        validate_features
    )

    assert required_features.passive is True

    assert required_result == {
        tense("PRESENT"),
        aspect("PERFECT")
    }

    assert validate_features.infinitive is True

    assert validate_result == set()

def test_past_perfect_passive_with_infinitive():

    doc = nlp(
        "The system had been required to validate the request."
    )

    required_token = next(
        token
        for token in doc
        if token.text == "required"
    )

    validate_token = next(
        token
        for token in doc
        if token.text == "validate"
    )

    required_features = VerbFeaturesExtractor.extract(
        required_token
    )

    validate_features = VerbFeaturesExtractor.extract(
        validate_token
    )

    required_result = VerbTenseClassifier.classify(
        required_features
    )

    validate_result = VerbTenseClassifier.classify(
        validate_features
    )

    assert required_features.passive is True

    assert required_result == {
        tense("PAST"),
        aspect("PERFECT")
    }

    assert validate_features.infinitive is True

    assert validate_result == set()

def test_future_perfect_passive_with_infinitive():

    doc = nlp(
        "The system will have been required to validate the request."
    )

    required_token = next(
        token
        for token in doc
        if token.text == "required"
    )

    validate_token = next(
        token
        for token in doc
        if token.text == "validate"
    )

    required_features = VerbFeaturesExtractor.extract(
        required_token
    )

    validate_features = VerbFeaturesExtractor.extract(
        validate_token
    )

    required_result = VerbTenseClassifier.classify(
        required_features
    )

    validate_result = VerbTenseClassifier.classify(
        validate_features
    )

    assert required_features.passive is True

    assert required_result == {
        tense("FUTURE"),
        aspect("PERFECT")
    }

    assert validate_features.infinitive is True

    assert validate_result == set()