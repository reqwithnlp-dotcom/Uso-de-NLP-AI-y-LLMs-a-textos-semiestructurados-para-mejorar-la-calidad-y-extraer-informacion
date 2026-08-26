import pytest

from analyzer.text_analyzer import TextAnalyzer
from models.error_code import ErrorCode


def test_valid_present_simple_should_not_report_issue():

    analyzer = TextAnalyzer()

    result = analyzer.analyze(
        "The cat hunts a mouse."
    )

    issues = [
        issue
        for context in result.contexts
        for issue in context.issues
    ]

    assert issues == []


def test_present_and_past_perfect_connected_with_and_should_report_mismatch():

    analyzer = TextAnalyzer()

    result = analyzer.analyze(
        "The cat hunts a mouse and had eaten it."
    )

    issues = [
        issue
        for context in result.contexts
        for issue in context.issues
    ]

    assert any(
        issue.error_code == ErrorCode.CONNECTOR_MISMATCH
        for issue in issues
    )


@pytest.mark.xfail(
    reason="Temporal expression consistency will be implemented separately."
)
def test_present_tense_with_yesterday_should_report_temporal_mismatch():

    analyzer = TextAnalyzer()

    result = analyzer.analyze(
        "The cat hunts the mouse yesterday."
    )

    issues = [
        issue
        for context in result.contexts
        for issue in context.issues
    ]

    assert issues