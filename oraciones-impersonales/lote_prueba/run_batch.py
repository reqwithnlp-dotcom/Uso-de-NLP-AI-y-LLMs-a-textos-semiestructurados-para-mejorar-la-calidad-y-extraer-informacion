"""
Corrida en lote: procesa lote_prueba/input.txt con el detector
y muestra el diagnóstico por consola.

Uso (desde la raíz del proyecto):
    python -m lote_prueba.run_batch
"""

from pathlib import Path

from model.detector import analyze_text

INPUT_FILE = Path(__file__).parent / "input.txt"


def _label(r):
    """Etiqueta legible a partir de los dos booleanos de la capa 1."""
    if r["ambiguous"]:
        return "AMBIGUO->capa2"
    return "PERSONAL" if r["personal"] else "IMPERSONAL"


def main():
    text = INPUT_FILE.read_text(encoding="utf-8")
    results = analyze_text(text)

    personales = impersonales = ambiguas = 0
    print(f"{'#':<4}{'Pers':<6}{'Imp':<6}{'Decisión':<16}{'Tipo':<22}Oración")
    print("-" * 100)
    for i, r in enumerate(results, 1):
        personales += r["personal"]
        impersonales += r["impersonal"]
        ambiguas += r["ambiguous"]
        print(
            f"{i:<4}{str(r['personal']):<6}{str(r['impersonal']):<6}"
            f"{_label(r):<16}{r['type']:<22}{r['sentence']}"
        )
    print("-" * 100)
    print(
        f"Total: {len(results)} | Personales: {personales} | "
        f"Impersonales: {impersonales} | Ambiguas (a capa 2): {ambiguas}"
    )


if __name__ == "__main__":
    main()
