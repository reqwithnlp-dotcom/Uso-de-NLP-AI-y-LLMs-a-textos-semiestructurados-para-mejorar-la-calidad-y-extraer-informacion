from servicio import detect_connectors, CONNECTORS


def test_basic_connectors():
    connectors, normal_words = detect_connectors("Dog and cat or rabbit", CONNECTORS)
    assert ("and", "addition") in connectors
    assert ("or", "disjunction") in connectors
    assert "dog" in normal_words
    assert "cat" in normal_words
    assert "rabbit" in normal_words


def test_multi_word_connector():
    connectors, normal_words = detect_connectors("As a result, she had to retake the exam.", CONNECTORS)
    assert ("as a result", "cause-effect") in connectors
    assert "she" in normal_words
    assert "as" not in normal_words
    assert "result" not in normal_words


def test_no_connectors():
    connectors, normal_words = detect_connectors("Today I went for a run.", CONNECTORS)
    assert connectors == []
    assert "today" in normal_words
    assert "run" in normal_words


def test_normalization():
    connectors, normal_words = detect_connectors("It was cold, HOWEVER; she went outside.", CONNECTORS)
    assert ("however", "contrast") in connectors
    assert "she" in normal_words


def test_empty_string():
    connectors, normal_words = detect_connectors("", CONNECTORS)
    assert connectors == []
    assert normal_words == []


if __name__ == "__main__":
    test_basic_connectors()
    test_multi_word_connector()
    test_no_connectors()
    test_normalization()
    test_empty_string()
    print("Todos los tests pasaron!")