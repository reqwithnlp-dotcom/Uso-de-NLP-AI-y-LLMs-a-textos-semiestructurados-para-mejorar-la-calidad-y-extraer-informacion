from model.detector import detectar_puntuacion_inusual


def test_normal_punctuation_returns_false_and_zero():
    assert detectar_puntuacion_inusual("Hi!") == (False, 0)


def test_adjacent_punctuation_is_reported():
    unusual, issues = detectar_puntuacion_inusual("Hi!.., Nice to meet you")

    assert unusual is True
    assert issues == ["!", ","]


def test_repeated_apostrophe_is_reported():
    unusual, issues = detectar_puntuacion_inusual("I don''t like tuna")

    assert unusual is True
    assert issues == ["'", "'"]


def test_unbalanced_brackets_are_reported():
    unusual, issues = detectar_puntuacion_inusual("Read this (carefully.")

    assert unusual is True
    assert issues == ["("]