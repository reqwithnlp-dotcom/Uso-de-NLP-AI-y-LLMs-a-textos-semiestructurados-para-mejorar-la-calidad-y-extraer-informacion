from povshift.detector import POVShiftDetector


def run_demo():
    detector = POVShiftDetector()

    samples = [
        (
            "John wondered where Mary was. Mary knew he was waiting.",
            "shift real",
        ),
        (
            "John wondered where Mary was. He felt nervous.",
            "sin shift (coreferencia)",
        ),
        (
            "John opened the door. Mary entered.",
            "sin shift (acción observable)",
        ),
        (
            "I felt nervous. You felt angry.",
            "shift deíctico con evidencia interna",
        ),
    ]

    for text, label in samples:
        print(f"\n--- {label} ---")
        print(text)
        shifts = detector.detect(text)
        if not shifts:
            print("Resultado: []")
            continue

        for shift in shifts:
            print("Resultado:")
            print(f"  from: {shift.from_character.canonical_name}")
            print(f"  to: {shift.to_character.canonical_name}")
            print(f"  sentence_index: {shift.sentence_index}")
            print(f"  confidence: {shift.confidence}")
            print(f"  evidence: {shift.evidence}")


if __name__ == "__main__":
    run_demo()
