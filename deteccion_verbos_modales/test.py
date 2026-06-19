from servicio import detect_modal_verbs, MODAL_VERBS


def test_single_modal():
    modals, phrases = detect_modal_verbs("She can swim very fast.", MODAL_VERBS)
    assert ("can", "ability") in modals
    assert "she" in phrases[0]
    assert "swim very fast" in phrases[1]


def test_multi_word_modal():
    modals, phrases = detect_modal_verbs("You ought to call her.", MODAL_VERBS)
    assert ("ought to", "obligation") in modals
    assert "you" in phrases[0]
    assert "call her" in phrases[1]


def test_multiple_modals():
    modals, phrases = detect_modal_verbs("You should call her because she might need help.", MODAL_VERBS)
    assert ("should", "recommendation") in modals
    assert ("might", "possibility") in modals
    assert len(modals) == 2
    assert len(phrases) == 3


def test_no_modals():
    modals, phrases = detect_modal_verbs("The dog runs in the park.", MODAL_VERBS)
    assert modals == []
    assert len(phrases) == 1
    assert "the dog runs in the park" in phrases[0]


def test_modal_at_start():
    modals, phrases = detect_modal_verbs("Will you come to the party?", MODAL_VERBS)
    assert ("will", "future") in modals
    assert "you come to the party" in phrases[0]


def test_have_to():
    modals, phrases = detect_modal_verbs("I have to finish this today.", MODAL_VERBS)
    assert ("have to", "obligation") in modals
    assert "i" in phrases[0]
    assert "finish this today" in phrases[1]