"""
Pasa las candidatas revisadas a mano a los .txt de data/raw/.

Lee training/data/review/candidates.csv (generado por mine_candidates.py),
toma las filas con `final_label` completo y las agrega al final de:

    PERSONAL   -> data/raw/personales.txt
    IMPERSONAL -> data/raw/impersonales.txt
    UNCLEAR    -> data/raw/unclear.txt

bajo un comentario "# --- minado <fecha> (<archivo>) ---". Las que ya
están en algún .txt se saltean, así que es seguro correrlo más de una vez.
Filas con `final_label` vacío = descartadas (no se importan).

Opción --accept-proposed: usa `proposed_label` cuando `final_label` está
vacío (solo para filas SIN conflicto). Útil para tandas grandes, pero
mete el ruido de la etiqueta silver: revisá al menos una muestra.

Uso (desde la raíz del servicio):

    python training/scripts/import_reviewed.py
    python training/scripts/import_reviewed.py --dry-run
"""

import argparse
import csv
from collections import Counter
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw"
DEFAULT_CSV = BASE / "data" / "review" / "candidates.csv"

TARGETS = {
    "PERSONAL": RAW / "personales.txt",
    "IMPERSONAL": RAW / "impersonales.txt",
    "UNCLEAR": RAW / "unclear.txt",
}
# Alias tolerados al revisar a mano en Excel
ALIASES = {"P": "PERSONAL", "I": "IMPERSONAL", "U": "UNCLEAR", "?": "UNCLEAR"}


def read_rows(path):
    raw = path.read_text(encoding="utf-8-sig")
    try:
        dialect = csv.Sniffer().sniff(raw.splitlines()[0], delimiters=";,\t")
    except csv.Error:
        dialect = csv.excel
    return list(csv.DictReader(raw.splitlines(), dialect=dialect))


def normalize(label):
    label = (label or "").strip().upper()
    return ALIASES.get(label, label)


def existing_sentences():
    seen = set()
    for p in TARGETS.values():
        if p.exists():
            for line in p.read_text(encoding="utf-8-sig").splitlines():
                s = line.strip()
                if s and not s.startswith("#"):
                    seen.add(s.lower())
    return seen


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    ap.add_argument("--accept-proposed", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="Muestra qué haría sin escribir")
    args = ap.parse_args()

    if not args.csv.exists():
        raise SystemExit(f"No existe {args.csv}. Corré primero mine_candidates.py")

    rows = read_rows(args.csv)
    seen = existing_sentences()
    to_add = {lab: [] for lab in TARGETS}
    stats = Counter()

    for r in rows:
        label = normalize(r.get("final_label"))
        if not label and args.accept_proposed and r.get("conflict") != "True":
            label = normalize(r.get("proposed_label"))
        if not label:
            stats["sin etiqueta"] += 1
            continue
        if label not in TARGETS:
            print(f"  AVISO: etiqueta desconocida {label!r} en id={r.get('id')} -> salteada")
            stats["etiqueta inválida"] += 1
            continue
        text = " ".join((r.get("text") or "").split())  # una sola línea
        if not text or text.lower() in seen:
            stats["ya existente"] += 1
            continue
        seen.add(text.lower())
        to_add[label].append(text)

    header = f"\n\n# --- minado {date.today().isoformat()} ({args.csv.name}) ---\n"
    for label, sents in to_add.items():
        print(f"  {label:<11} +{len(sents)}")
        if sents and not args.dry_run:
            with open(TARGETS[label], "a", encoding="utf-8") as f:
                f.write(header + "\n".join(sents) + "\n")
    for k, v in stats.items():
        print(f"  ({k}: {v})")
    if args.dry_run:
        print("\n--dry-run: no se escribió nada.")
    else:
        print("\nListo. Siguiente paso: python training/scripts/build_corpus.py")


if __name__ == "__main__":
    main()
