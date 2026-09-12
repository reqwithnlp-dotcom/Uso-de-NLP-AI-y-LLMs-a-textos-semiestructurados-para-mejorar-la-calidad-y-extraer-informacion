from povshift.detector import POVShiftDetector


def run_demo():
    detector = POVShiftDetector()

    samples = [
        (
            "John wondered where Mary was. Mary knew he was waiting.",
            "TC-13: shift real",
        ),
        (
            "John wondered where Mary was. He felt nervous.",
            "TC-14: sin shift por coreferencia",
        ),
        (
            "John opened the door. Mary entered.",
            "TC-15: sin shift por acción observable",
        ),
        (
            "I felt nervous. You felt angry.",
            "TC-17: shift deíctico con evidencia interna",
        ),
        (
            "John feared that Mary had left. He remembered her promise and felt anxious.",
            "Ejemplo más complejo: foco sostenido con emoción y recuerdo",
        ),
        (
            "John thought Mary was late. She knew he was waiting outside. He felt relieved when she finally arrived.",
            "Ejemplo más complejo: cambio de foco con evidencia múltiple",
        ),
        (
            "Mary saw John leave. She knew he was angry. John hoped she would forgive him.",
            "Ejemplo más complejo: cambio de foco de Mary a John",
        ),
        (
            "John opened the door. Mary smiled. She was glad he had come.",
            "Ejemplo más complejo: acción + emoción sin shift real",
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
