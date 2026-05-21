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


def detect_connectors(text: str) -> list[tuple[str, str]]:
    normalized = normalize(text)
    found = []
    matched_positions = set()

    for phrase in MULTI_WORD:
        for match in re.finditer(r"\b" + re.escape(phrase) + r"\b", normalized):
            positions = set(range(match.start(), match.end()))
            if not positions & matched_positions:
                matched_positions |= positions
                found.append((match.start(), phrase, CONNECTORS[phrase]))

    for word in SINGLE_WORD:
        for match in re.finditer(r"\b" + re.escape(word) + r"\b", normalized):
            positions = set(range(match.start(), match.end()))
            if not positions & matched_positions:
                matched_positions |= positions
                found.append((match.start(), word, CONNECTORS[word]))

    found.sort(key=lambda x: x[0])

    return [(word, type_) for _, word, type_ in found]


if __name__ == "__main__":
    examples = [
        "Dog and cat or rabbit",
        "I wanted to go for a run; however, it was raining, so I stayed at home.",
        "Today I went for a run.",
        "She studied hard; therefore, she passed. Furthermore, she got an A.",
    ]

    for sentence in examples:
        connectors = detect_connectors(sentence)
        print(f"Input:      {sentence}")
        print(f"Connectors: {connectors}")
        print()