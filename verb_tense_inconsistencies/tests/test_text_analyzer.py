from analyzer.text_analyzer import TextAnalyzer


def test_should_normalize_and_split_text():

    analyzer = TextAnalyzer()

    text = (
        "I've submitted the request. "
        "The system doesn't validate it."
    )

    result = analyzer.analyze(text)

    assert result["normalized_text"] == (
        "I have submitted the request. "
        "The system does not validate it."
    )

    assert len(result["fragments"]) == 2

    assert result["issues"] == []