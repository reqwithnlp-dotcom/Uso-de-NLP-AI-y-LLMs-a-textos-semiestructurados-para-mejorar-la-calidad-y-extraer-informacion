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
    """Etiqueta legible de la capa 1."""
    if r["ambiguous"]:
        return "AMBIGUO->capa2"
    return "PERSONAL" if r["personal"] else "IMPERSONAL"


def _final(r):
    """Decisión final + quién la tomó (y el score si fue la capa 2)."""
    if r["decided_by"] == "layer2":
        return f"{r['final_label']} (c2 {r['layer2_scores'][r['final_label']]:.2f})"
    return f"{r['final_label']} ({r['decided_by']})"


def main():
    text = INPUT_FILE.read_text(encoding="utf-8")
    results = analyze_text(text)

    personales = impersonales = ambiguas = resueltas_c2 = 0
    print(f"{'#':<4}{'Pers':<6}{'Imp':<6}{'Capa 1':<16}{'Tipo':<20}{'Final':<24}Oración")
    print("-" * 120)
    for i, r in enumerate(results, 1):
        personales += r["personal"]
        impersonales += r["impersonal"]
        ambiguas += r["ambiguous"]
        resueltas_c2 += r["decided_by"] == "layer2"
        print(
            f"{i:<4}{str(r['personal']):<6}{str(r['impersonal']):<6}"
            f"{_label(r):<16}{r['type']:<20}{_final(r):<24}{r['sentence']}"
        )
    print("-" * 120)
    print(
        f"Total: {len(results)} | Personales: {personales} | "
        f"Impersonales: {impersonales} | Ambiguas (a capa 2): {ambiguas} | "
        f"Resueltas por capa 2: {resueltas_c2}"
    )


if __name__ == "__main__":
    main()
