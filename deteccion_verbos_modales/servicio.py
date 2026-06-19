import re

MODAL_VERBS = {
    # Ability
    "can": "ability",
    "could": "ability/possibility",

    # Permission / Possibility
    "may": "permission/possibility",
    "might": "possibility",

    # Obligation
    "must": "obligation",
    "shall": "future/obligation",
    "should": "recommendation",
    "ought to": "obligation",
    "have to": "obligation",
    "need to": "necessity",

    # Future / Conditional
    "will": "future",
    "would": "conditional",

    # Past habit
    "used to": "past habit",
}


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[.,;:!?'\"()\[\]]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def detect_modal_verbs(text: str, modals: dict = MODAL_VERBS) -> tuple[list[tuple[str, str]], list[str]]:
    multi_word = sorted([k for k in modals if " " in k], key=lambda x: -len(x.split()))
    single_word = [k for k in modals if " " not in k]

    normalized = normalize(text)
    found = []
    matched_positions = set()

    for phrase in multi_word:
        for match in re.finditer(r"\b" + re.escape(phrase) + r"\b", normalized):
            positions = set(range(match.start(), match.end()))
            if not positions & matched_positions:
                matched_positions |= positions
                found.append((match.start(), phrase, modals[phrase]))

    for word in single_word:
        for match in re.finditer(r"\b" + re.escape(word) + r"\b", normalized):
            positions = set(range(match.start(), match.end()))
            if not positions & matched_positions:
                matched_positions |= positions
                found.append((match.start(), word, modals[word]))

    found.sort(key=lambda x: x[0])
    modal_list = [(word, type_) for _, word, type_ in found]

    # Frases entre los verbos modales
    split_points = [(pos, pos + len(phrase)) for pos, phrase, _ in found]

    phrases = []
    prev_end = 0
    for start, end in split_points:
        fragment = normalized[prev_end:start].strip()
        if fragment:
            phrases.append(fragment)
        prev_end = end

    last_fragment = normalized[prev_end:].strip()
    if last_fragment:
        phrases.append(last_fragment)

    return modal_list, phrases


if __name__ == "__main__":
    print("=== Modal Verb Detector ===")
    print("Escribi 'salir' para terminar.\n")
    while True:
        text = input("Ingresa una oracion: ")
        if text.strip().lower() == "salir":
            print("Saliendo...")
            break

        if text.strip() == "":
            print("Por favor ingresa una oracion.\n")
            continue

        modals, phrases = detect_modal_verbs(text)
        print(f"Modal verbs:  {modals}")
        print(f"Phrases:      {phrases}\n")