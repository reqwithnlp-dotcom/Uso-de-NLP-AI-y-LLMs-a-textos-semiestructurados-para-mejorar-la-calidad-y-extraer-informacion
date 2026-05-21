from servicio import detect_connectors, CONNECTORS

def test_basic_connectors():
    result = detect_connectors("Dog and cat or rabbit", CONNECTORS)
    assert ("and", "addition") in result
    assert ("or", "disjunction") in result

def test_multi_word_connector():
    result = detect_connectors("As a result, she had to retake the exam.", CONNECTORS)
    assert ("as a result", "cause-effect") in result

def test_no_connectors():
    result = detect_connectors("Today I went for a run.", CONNECTORS)
    assert result == []

def test_normalization():
    result = detect_connectors("It was cold, HOWEVER; she went outside.", CONNECTORS)
    assert ("however", "contrast") in result

def test_empty_string():
    result = detect_connectors("", CONNECTORS)
    assert result == []
if __name__ == "__main__":
    test_basic_connectors()
    test_multi_word_connector()
    test_no_connectors()
    test_normalization()
    test_empty_string()
    print("Todos los tests pasaron!")   