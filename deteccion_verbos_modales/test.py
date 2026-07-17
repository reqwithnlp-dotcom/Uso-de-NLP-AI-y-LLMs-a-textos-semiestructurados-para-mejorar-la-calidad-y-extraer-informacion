from servicio import extract_modal_actions, MODAL_CATEGORIES


def test_single_modal():
    results = extract_modal_actions("She can swim very fast.")
    assert len(results) == 1
    assert results[0]["modal"] == "can"
    assert results[0]["category"] == "possibility/permission"
    assert "swim very fast" in results[0]["action"]


def test_multi_word_modal():
    results = extract_modal_actions("You ought to call her.")
    assert len(results) == 1
    assert results[0]["modal"] == "ought to"
    assert results[0]["category"] == "recommendation"
    assert "call her" in results[0]["action"]


def test_multiple_modals():
    results = extract_modal_actions("You should call her because she might need help.")
    assert len(results) == 2

    modals = [(r["modal"], r["category"]) for r in results]
    assert ("should", "recommendation") in modals
    assert ("might", "possibility/permission") in modals

    # la accion de "should" arranca justo despues del modal
    should_result = next(r for r in results if r["modal"] == "should")
    assert "call her" in should_result["action"]

    # la accion de "might" arranca despues de ese modal
    might_result = next(r for r in results if r["modal"] == "might")
    assert "need help" in might_result["action"]


def test_no_modals():
    results = extract_modal_actions("The dog runs in the park.")
    assert results == []


def test_modal_at_start():
    # "will" no esta en MODAL_CATEGORIES (esta en STOPWORDS), no deberia detectarse
    results = extract_modal_actions("Will you come to the party?")
    assert results == []


def test_have_to():
    results = extract_modal_actions("I have to finish this today.")
    assert len(results) == 1
    assert results[0]["modal"] == "have to"
    assert results[0]["category"] == "obligation"
    assert "finish this today" in results[0]["action"]


def test_prohibition_detected():
    # caso nuevo: la categoria "prohibition" no existia en los tests viejos
    results = extract_modal_actions("Visitors cannot access the server room.")
    assert len(results) == 1
    assert results[0]["modal"] == "cannot"
    assert results[0]["category"] == "prohibition"
    assert "access the server room" in results[0]["action"]


def test_modal_categories_structure():
    # sanity check: confirma que las categorias esperadas siguen existiendo
    assert set(MODAL_CATEGORIES.keys()) == {
        "prohibition", "obligation", "recommendation", "possibility/permission"
    }