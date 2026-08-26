import spacy

from extractors.verb_features_extractor import VerbFeaturesExtractor


nlp = spacy.load("en_core_web_sm")


def get_verb(sentence, text):

    doc = nlp(sentence)

    return next(
        token
        for token in doc
        if token.text == text
    )


def test_present_perfect():

    token = get_verb(
        "The system has validated the request.",
        "validated"
    )

    features = VerbFeaturesExtractor.extract(token)

    assert features.verb_tag == "VBN"

    assert [
        auxiliary.text.lower()
        for auxiliary in features.auxiliaries
    ] == ["has"]

    assert features.passive is False
    assert features.negated is False
    assert features.infinitive is False

def test_present_perfect_continuous():

    token = get_verb(
        "The system has been validating the request.",
        "validating"
    )

    features = VerbFeaturesExtractor.extract(token)

    assert features.verb_tag == "VBG"

    assert [
        aux.text.lower()
        for aux in features.auxiliaries
    ] == ["has", "been"]


def test_negative_present_simple():

    token = get_verb(
        "The system does not validate the request.",
        "validate"
    )

    features = VerbFeaturesExtractor.extract(token)

    assert features.verb_tag == "VB"

    assert [
        aux.text.lower()
        for aux in features.auxiliaries
    ] == ["does"]

    assert features.negated is True


def test_passive():

    token = get_verb(
        "The request has been validated by the system.",
        "validated"
    )

    features = VerbFeaturesExtractor.extract(token)

    assert features.verb_tag == "VBN"

    assert [
        aux.text.lower()
        for aux in features.auxiliaries
    ] == ["has", "been"]

    assert features.passive is True

def test_present_simple():

    token = get_verb(
        "The system validates the request.",
        "validates"
    )

    features = VerbFeaturesExtractor.extract(token)

    assert features.verb_tag == "VBZ"
    assert features.auxiliaries == []
    assert features.passive is False
    assert features.negated is False
    assert features.infinitive is False


def test_modal():

    token = get_verb(
        "The system should validate the request.",
        "validate"
    )

    features = VerbFeaturesExtractor.extract(token)

    assert features.verb_tag == "VB"

    assert [
        aux.text.lower()
        for aux in features.auxiliaries
    ] == ["should"]

    assert features.passive is False
    assert features.negated is False
    assert features.infinitive is False


def test_modal_perfect():

    token = get_verb(
        "The system should have validated the request.",
        "validated"
    )

    features = VerbFeaturesExtractor.extract(token)

    assert features.verb_tag == "VBN"

    assert [
        aux.text.lower()
        for aux in features.auxiliaries
    ] == ["should", "have"]

    assert features.passive is False
    assert features.negated is False
    assert features.infinitive is False


def test_have_to_structure():

    token = get_verb(
        "The system has to validate the request.",
        "validate"
    )

    features = VerbFeaturesExtractor.extract(token)

    assert features.verb_tag == "VB"
    assert features.auxiliaries == []
    assert features.infinitive is True

    assert features.passive is False
    assert features.negated is False


def test_coordinated_verbs():

    sentence = (
        "The user has submitted the request "
        "and the system validates it."
    )

    submitted = get_verb(sentence, "submitted")
    validates = get_verb(sentence, "validates")

    submitted_features = VerbFeaturesExtractor.extract(submitted)
    validates_features = VerbFeaturesExtractor.extract(validates)

    assert submitted_features.verb_tag == "VBN"

    assert [
        aux.text.lower()
        for aux in submitted_features.auxiliaries
    ] == ["has"]

    assert validates_features.verb_tag == "VBZ"
    assert validates_features.auxiliaries == []