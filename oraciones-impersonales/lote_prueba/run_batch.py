"""
Corrida en lote: procesa lote_prueba/input.txt con el detector
y muestra el diagnóstico por consola.

Uso (desde la raíz del proyecto):
    python -m lote_prueba.run_batch
"""

from pathlib import Path

from model.detector import analyze_text

INPUT_FILE = Path(__file__).parent / "input.txt"


def main():
    text = INPUT_FILE.read_text(encoding="utf-8")
    results = analyze_text(text)

    impersonales = 0
    print(f"{'#':<4}{'¿Impersonal?':<14}{'Tipo':<22}Oración")
    print("-" * 90)
    for i, r in enumerate(results, 1):
        flag = "True" if r["impersonal"] else "False"
        impersonales += r["impersonal"]
        print(f"{i:<4}{flag:<14}{r['type']:<22}{r['sentence']}")
    print("-" * 90)
    print(f"Total: {len(results)} oraciones | Impersonales: {impersonales}")


if __name__ == "__main__":
    main()
