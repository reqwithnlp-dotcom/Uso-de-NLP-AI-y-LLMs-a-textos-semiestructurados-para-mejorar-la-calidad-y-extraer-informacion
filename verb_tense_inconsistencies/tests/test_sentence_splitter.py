from analyzer.sentence_splitter import SentenceSplitter


def test_should_split_two_sentences():

    text = (
        "The user submits the request. "
        "The system validates the request."
    )

    result = SentenceSplitter.split(text)

    assert len(result) == 2

    assert result[0].text == "The user submits the request."
    assert result[1].text == "The system validates the request."


def test_should_keep_single_sentence():

    text = "The user submits the request."

    result = SentenceSplitter.split(text)

    assert len(result) == 1


def test_should_return_positions():

    text = (
        "The user submits the request. "
        "The system validates the request."
    )

    result = SentenceSplitter.split(text)

    assert result[0].start_char == 0

    assert result[0].end_char > result[0].start_char

def test_should_split_complex_requirement_document():

    text = """
    The system shall calculate the final price using a tax rate of 3.75%.
    If the calculated value exceeds 1500.50 USD, the system shall notify the user.

    The user can update the order information at any time.
    However, changes made after 10.30 p.m. will not be applied until the next business day.

    The inventory service validates stock availability and generates a reservation.
    """

    result = SentenceSplitter.split(text)

    assert len(result) == 5

    assert result[0].text == (
        "The system shall calculate the final price using a tax rate of 3.75%."
    )

    assert result[1].text == (
        "If the calculated value exceeds 1500.50 USD, the system shall notify the user."
    )

    assert result[2].text == (
        "The user can update the order information at any time."
    )

    assert result[3].text == (
        "However, changes made after 10.30 p.m. will not be applied until the next business day."
    )

    assert result[4].text == (
        "The inventory service validates stock availability and generates a reservation."
    )