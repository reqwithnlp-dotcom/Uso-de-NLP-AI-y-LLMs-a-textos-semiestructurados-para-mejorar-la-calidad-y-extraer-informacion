from analyzer.normalizer import TextNormalizer


def test_should_expand_negative_contraction():

    text = "The system doesn't validate the request."

    result = TextNormalizer.normalize(text)

    assert result == "The system does not validate the request."


def test_should_expand_have_contraction():

    text = "I've completed the task."

    result = TextNormalizer.normalize(text)

    assert result == "I have completed the task."


def test_should_expand_will_contraction():

    text = "The user won't receive the notification."

    result = TextNormalizer.normalize(text)

    assert result == "The user will not receive the notification."