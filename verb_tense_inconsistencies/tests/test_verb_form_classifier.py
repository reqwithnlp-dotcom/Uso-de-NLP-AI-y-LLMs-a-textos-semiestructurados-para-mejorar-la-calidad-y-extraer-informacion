from classifiers.verb_form_classifier import VerbFormClassifier

def test_validate_should_not_be_valid_vbn():
    assert VerbFormClassifier.is_valid_form(
        word="validate",
        lemma="validate",
        expected_tag="VBN"
    ) is False


def test_validated_should_be_valid_vbn():
    assert VerbFormClassifier.is_valid_form(
        word="validated",
        lemma="validate",
        expected_tag="VBN"
    ) is True


def test_load_should_not_be_valid_vbn():
    assert VerbFormClassifier.is_valid_form(
        word="load",
        lemma="load",
        expected_tag="VBN"
    ) is False


def test_loaded_should_be_valid_vbn():
    assert VerbFormClassifier.is_valid_form(
        word="loaded",
        lemma="load",
        expected_tag="VBN"
    ) is True


def test_generate_should_not_be_valid_vbg():
    assert VerbFormClassifier.is_valid_form(
        word="generate",
        lemma="generate",
        expected_tag="VBG"
    ) is False


def test_generating_should_be_valid_vbg():
    assert VerbFormClassifier.is_valid_form(
        word="generating",
        lemma="generate",
        expected_tag="VBG"
    ) is True

def test_submitted_should_be_valid_vbn():
    assert VerbFormClassifier.is_valid_form(
        word="submitted",
        lemma="submit",
        expected_tag="VBN"
    ) is True


def test_submit_should_not_be_valid_vbn():
    assert VerbFormClassifier.is_valid_form(
        word="submit",
        lemma="submit",
        expected_tag="VBN"
    ) is False