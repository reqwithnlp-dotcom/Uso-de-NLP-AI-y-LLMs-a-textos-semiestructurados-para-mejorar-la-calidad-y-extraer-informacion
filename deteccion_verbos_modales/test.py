from servicio import (
    extract_modal_actions,
    find_consistencies_and_inconsistencies,
    analyze_text,
    MODAL_CATEGORIES,
)


def test_extract_single_modal():
    results = extract_modal_actions("Employees can request time off.")
    assert len(results) == 1
    assert results[0]["modal"] == "can"
    assert results[0]["category"] == "possibility/permission"
    assert "request time off" in results[0]["action"]


def test_extract_multi_word_modal():
    results = extract_modal_actions("Employees have to submit the form.")
    assert len(results) == 1
    assert results[0]["modal"] == "have to"
    assert results[0]["category"] == "obligation"
    assert "submit the form" in results[0]["action"]


def test_extract_multiple_sentences():
    text = "Employees can request time off. Managers must approve requests within 48 hours."
    results = extract_modal_actions(text)
    assert len(results) == 2
    modals = [r["modal"] for r in results]
    assert "can" in modals
    assert "must" in modals


def test_no_modals():
    results = extract_modal_actions("The dog runs in the park.")
    assert results == []


def test_prohibition_not_confused_with_obligation():
    # "must not" tiene que matchear como prohibición, no como "must" (obligación)
    results = extract_modal_actions("Employees must not access the server after hours.")
    assert len(results) == 1
    assert results[0]["modal"] == "must not"
    assert results[0]["category"] == "prohibition"


def test_detects_inconsistency_between_permission_and_obligation():
    text = (
        "Employees can request time off through the online portal. "
        "Employees must request time off through the online portal at least three days in advance."
    )
    consistencies, inconsistencies = find_consistencies_and_inconsistencies(
        extract_modal_actions(text)
    )
    assert len(inconsistencies) == 1
    categories = {inconsistencies[0]["case_1"]["category"], inconsistencies[0]["case_2"]["category"]}
    assert categories == {"possibility/permission", "obligation"}


def test_detects_consistency_between_same_category():
    text = (
        "Employees can request time off through the online portal. "
        "Employees can also request time off through the online portal for medical reasons."
    )
    consistencies, inconsistencies = find_consistencies_and_inconsistencies(
        extract_modal_actions(text)
    )
    assert len(consistencies) == 1
    assert inconsistencies == []
    assert consistencies[0]["case_1"]["category"] == "possibility/permission"
    assert consistencies[0]["case_2"]["category"] == "possibility/permission"


def test_unrelated_actions_produce_no_matches():
    text = (
        "Employees can request time off through the online portal. "
        "The office is located on the third floor of the building."
    )
    consistencies, inconsistencies = find_consistencies_and_inconsistencies(
        extract_modal_actions(text)
    )
    assert consistencies == []
    assert inconsistencies == []


def test_analyze_text_returns_two_lists():
    text = (
        "Employees can request time off through the online portal. "
        "Employees must request time off through the online portal at least three days in advance."
    )
    consistencies, inconsistencies = analyze_text(text)
    assert isinstance(consistencies, list)
    assert isinstance(inconsistencies, list)
    assert len(inconsistencies) == 1
    assert len(consistencies) == 0


def test_modal_categories_structure():
    # Confirma que las 4 categorías esperadas existen
    assert set(MODAL_CATEGORIES.keys()) == {
        "prohibition", "obligation", "recommendation", "possibility/permission"
    }