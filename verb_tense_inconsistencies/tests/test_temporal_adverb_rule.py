from analyzer.text_analyzer import TextAnalyzer
from models.error_code import ErrorCode


def analyze(text):
    return TextAnalyzer().analyze(text).contexts[0]


def has_temporal_error(context):
    return any(
        issue.error_code == ErrorCode.TEMPORAL_ADVERB_MISMATCH
        for issue in context.issues
    )


def test_adverb_extractor_stores_temporal_tokens_in_context():
    context = analyze("The system validates the request tomorrow.")

    assert [adverb.text for adverb in context.advberbs] == ["tomorrow"]


def test_past_simple_with_future_adverb_is_incompatible():
    context = analyze(
        "The system validated the request tomorrow."
    )

    assert has_temporal_error(context)


def test_future_simple_with_past_adverb_is_incompatible():
    context = analyze(
        "The system will validate the request yesterday."
    )

    assert has_temporal_error(context)


def test_past_simple_with_past_adverb_is_accepted():
    context = analyze(
        "The system validated the request yesterday."
    )

    assert not has_temporal_error(context)


def test_present_simple_with_future_adverb_is_accepted():
    context = analyze(
        "The system validates the request tomorrow."
    )

    assert not has_temporal_error(context)


def test_present_perfect_with_past_adverb_is_incompatible():
    context = analyze(
        "The system has validated the request yesterday."
    )

    assert has_temporal_error(context)


def test_present_perfect_with_recently_is_accepted():
    context = analyze(
        "The system has recently validated the request."
    )

    assert not has_temporal_error(context)


def test_non_temporal_adverb_does_not_report_error():
    context = analyze(
        "The system carefully validates the request."
    )

    assert context.advberbs == []

    assert not has_temporal_error(context)