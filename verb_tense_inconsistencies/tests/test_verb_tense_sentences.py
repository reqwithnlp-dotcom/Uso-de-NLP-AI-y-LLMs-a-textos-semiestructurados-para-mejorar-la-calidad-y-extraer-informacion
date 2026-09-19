import pytest


@pytest.mark.parametrize(
    "tense, affirmative, negative, question",
    [
        (
            "present_simple",
            "The system validates the request.",
            "The system does not validate the request.",
            "Does the system validate the request?",
        ),
        (
            "present_continuous",
            "The system is validating the request.",
            "The system is not validating the request.",
            "Is the system validating the request?",
        ),
        (
            "present_perfect",
            "The system has validated the request.",
            "The system has not validated the request.",
            "Has the system validated the request?",
        ),
        (
            "present_perfect_continuous",
            "The system has been validating the request.",
            "The system has not been validating the request.",
            "Has the system been validating the request?",
        ),
        (
            "past_simple",
            "The system validated the request.",
            "The system did not validate the request.",
            "Did the system validate the request?",
        ),
        (
            "past_continuous",
            "The system was validating the request.",
            "The system was not validating the request.",
            "Was the system validating the request?",
        ),
        (
            "past_perfect",
            "The system had validated the request.",
            "The system had not validated the request.",
            "Had the system validated the request?",
        ),
        (
            "past_perfect_continuous",
            "The system had been validating the request.",
            "The system had not been validating the request.",
            "Had the system been validating the request?",
        ),
        (
            "future_simple",
            "The system will validate the request.",
            "The system will not validate the request.",
            "Will the system validate the request?",
        ),
        (
            "future_continuous",
            "The system will be validating the request.",
            "The system will not be validating the request.",
            "Will the system be validating the request?",
        ),
        (
            "future_perfect",
            "The system will have validated the request.",
            "The system will not have validated the request.",
            "Will the system have validated the request?",
        ),
        (
            "future_perfect_continuous",
            "The system will have been validating the request.",
            "The system will not have been validating the request.",
            "Will the system have been validating the request?",
        ),
    ],
)
def test_verb_tense_sentence_cases(
    tense,
    affirmative,
    negative,
    question,
):
    assert affirmative
    assert negative
    assert question