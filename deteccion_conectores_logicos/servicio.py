import re

CONNECTORS = {
    # Addition
    "and": "addition",
    "also": "addition",
    "furthermore": "addition",
    "moreover": "addition",
    "besides": "addition",
    "additionally": "addition",
    "too": "addition",
    "in addition": "addition",
    "as well as": "addition",

    # Disjunction
    "or": "disjunction",
    "either": "disjunction",
    "neither": "disjunction",
    "nor": "disjunction",
    "otherwise": "disjunction",

    # Contrast
    "but": "contrast",
    "however": "contrast",
    "although": "contrast",
    "though": "contrast",
    "whereas": "contrast",
    "while": "contrast",
    "nevertheless": "contrast",
    "nonetheless": "contrast",
    "yet": "contrast",
    "despite": "contrast",
    "still": "contrast",
    "even though": "contrast",
    "on the other hand": "contrast",
    "in contrast": "contrast",
    "on the contrary": "contrast",

    # Cause-effect
    "so": "cause-effect",
    "therefore": "cause-effect",
    "thus": "cause-effect",
    "hence": "cause-effect",
    "consequently": "cause-effect",
    "because": "cause-effect",
    "since": "cause-effect",
    "accordingly": "cause-effect",
    "as a result": "cause-effect",
    "due to": "cause-effect",
    "for this reason": "cause-effect",

    # Sequence
    "first": "sequence",
    "second": "sequence",
    "third": "sequence",
    "then": "sequence",
    "next": "sequence",
    "finally": "sequence",
    "afterward": "sequence",
    "subsequently": "sequence",
    "lastly": "sequence",
    "to begin with": "sequence",

    # Exemplification
    "namely": "exemplification",
    "for example": "exemplification",
    "for instance": "exemplification",
    "such as": "exemplification",
    "in other words": "exemplification",
    "that is": "exemplification",

    # Conclusion
    "overall": "conclusion",
    "in conclusion": "conclusion",
    "in summary": "conclusion",
    "to sum up": "conclusion",
    "in short": "conclusion",
    "to conclude": "conclusion",

    # Condition
    "if": "condition",
    "unless": "condition",
    "provided that": "condition",
    "as long as": "condition",
    "in case": "condition",
}

MULTI_WORD = sorted([k for k in CONNECTORS if " " in k], key=lambda x: -len(x.split()))
SINGLE_WORD = [k for k in CONNECTORS if " " not in k]


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[.,;:!?'\"()\[\]]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def detect_connectors(text: str, connectors: dict[str, str] = CONNECTORS) -> tuple[list[tuple[str, str]], list[str]]:
    multi_word = sorted([k for k in connectors if " " in k], key=lambda x: -len(x.split()))
    single_word = [k for k in connectors if " " not in k]

    normalized = normalize(text)
    found = []
    matched_positions = set()

    # Detectar frases multi-palabra primero
    for phrase in multi_word:
        for match in re.finditer(r"\b" + re.escape(phrase) + r"\b", normalized):
            positions = set(range(match.start(), match.end()))
            if not positions & matched_positions:
                matched_positions |= positions
                found.append((match.start(), phrase, connectors[phrase]))

    # Detectar palabras individuales
    for word in single_word:
        for match in re.finditer(r"\b" + re.escape(word) + r"\b", normalized):
            positions = set(range(match.start(), match.end()))
            if not positions & matched_positions:
                matched_positions |= positions
                found.append((match.start(), word, connectors[word]))

    found.sort(key=lambda x: x[0])
    connector_list = [(word, type_) for _, word, type_ in found]

    # Armar el set de todas las palabras que forman parte de conectores detectados
    connector_words = set()
    for _, phrase, _ in found:
        for w in phrase.split():
            connector_words.add(w)

    # Normal words: palabras del texto normalizado que no son parte de ningún conector
    all_words = normalized.split()
    normal_words = [w for w in all_words if w not in connector_words]

    return connector_list, normal_words


if __name__ == "__main__":
    print("=== Logical Connector Detector ===")
    print("Escribi 'salir' para terminar.\n")
    while True:
        text = input("Ingresa una oracion: ")
        if text.strip().lower() == "salir":
            print("Saliendo...")
            break

        if text.strip() == "":
            print("Por favor ingresa una oracion.\n")
            continue

        connectors, normal_words = detect_connectors(text)
        print(f"Connectors:   {connectors}")
        print(f"Normal words: {normal_words}\n")