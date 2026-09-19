import pytest

from analyzer.text_analyzer import TextAnalyzer
from models.error_code import ErrorCode


def get_connector_issues(text):

    result = TextAnalyzer().analyze(text)

    return [
        issue
        for context in result.contexts
        for issue in context.issues
        if issue.error_code == ErrorCode.CONNECTOR_MISMATCH
    ]


def test_same_tense_with_and_should_be_valid():

    issues = get_connector_issues(
        "The cat hunts a mouse and eats it."
    )

    assert issues == []


def test_present_and_past_with_and_should_report_mismatch():

    issues = get_connector_issues(
        "The cat hunts a mouse and had eaten it."
    )

    assert len(issues) == 1


def test_same_tense_with_or_should_be_valid():

    issues = get_connector_issues(
        "The system validates the request or rejects it."
    )

    assert issues == []


def test_present_and_past_with_or_should_report_mismatch():

    issues = get_connector_issues(
        "The system validates the request or rejected it."
    )

    assert len(issues) == 1


def test_same_tense_with_but_should_be_valid():

    issues = get_connector_issues(
        "The system validates the request but stores the result."
    )

    assert issues == []


def test_present_and_past_with_but_should_report_mismatch():

    issues = get_connector_issues(
        "The system validates the request but stored the result."
    )

    assert len(issues) == 1


def test_three_verbs_same_tense_should_be_valid():

    issues = get_connector_issues(
        "The system validates the request, stores it and sends a notification."
    )

    assert issues == []


def test_three_verbs_with_one_different_tense_should_report_mismatch():

    issues = get_connector_issues(
        "The system validates the request, stored it and sends a notification."
    )

    assert len(issues) >= 1