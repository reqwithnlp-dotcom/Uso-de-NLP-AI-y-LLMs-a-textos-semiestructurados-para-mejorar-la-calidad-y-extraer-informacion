"""
Construye el corpus de entrenamiento a partir de los .txt escritos a mano.

Pasos:
    1. Lee data/raw/personales.txt e impersonales.txt (una oración por línea).
    2. Controla calidad: duplicados, balance de clases, líneas sospechosas.
    3. Parte en train/dev/test de forma estratificada por clase.
    4. Exporta a DocBin (.spacy), el formato que consume `spacy train`.

Uso (desde la raíz del servicio, la carpeta que contiene main.py):

    python training/scripts/build_corpus.py

Salida: training/data/corpus/{train,dev,test}.spacy  (+ los .jsonl equivalentes)
"""

import json
import random
from collections import defaultdict
from pathlib import Path

import spacy
from spacy.tokens import DocBin

# Las dos etiquetas del clasificador. UNCLEAR no entra al entrenamiento.
LABELS = ["PERSONAL", "IMPERSONAL"]

# Proporciones del split (el resto de train va a dev)
TEST_RATIO = 0.10
DEV_RATIO = 0.10

SEED = 42  # fijo, para que el split sea reproducible

BASE = Path(__file__).resolve().parents[1]  # .../training
RAW = BASE / "data" / "raw"
CORPUS = BASE / "data" / "corpus"

SOURCES = {
    "PERSONAL": RAW / "personales.txt",
    "IMPERSONAL": RAW / "impersonales.txt",
}


def read_sentences(path, label):
    """Lee un .txt de oraciones. Ignora vacías y comentarios (#)."""
    if not path.exists():
        raise SystemExit(f"Falta el archivo {path}")

    rows = []
    # utf-8-sig tolera el BOM que agrega el Bloc de notas en Windows
    for n, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        text = line.strip()
        if not text or text.startswith("#"):
            continue
        rows.append({"text": text, "label": label, "source": path.name, "line": n})
    return rows


def check_quality(rows):
    """Avisa de problemas típicos de un corpus escrito a mano."""
    print(f"\nTotal de oraciones: {len(rows)}")
    for label in LABELS:
        n = sum(r["label"] == label for r in rows)
        pct = 100 * n / len(rows) if rows else 0
        print(f"  {label:<12} {n:>5}  ({pct:.1f}%)")

    # Duplicados: si una cae en train y otra en test, inflan las métricas
    seen, dups = {}, []
    for r in rows:
        key = r["text"].lower()
        if key in seen:
            dups.append((r["text"], seen[key], f"{r['source']}:{r['line']}"))
        else:
            seen[key] = f"{r['source']}:{r['line']}"
    if dups:
        print(f"\n  AVISO: {len(dups)} oración(es) duplicada(s):")
        for text, first, second in dups[:10]:
            print(f"    - {text!r}  ({first} y {second})")

    # Líneas que parecen numeradas o cortadas a la mitad
    for r in rows:
        if r["text"][0].isdigit() or r["text"].startswith(("-", "*")):
            print(f"  AVISO: ¿línea numerada? {r['source']}:{r['line']} -> {r['text']!r}")

    # Desbalance fuerte
    counts = [sum(r["label"] == lab for r in rows) for lab in LABELS]
    if counts and min(counts) and max(counts) / min(counts) > 1.5:
        print("\n  AVISO: clases desbalanceadas (>1.5x). Emparejalas si podés.")


def split(rows):
    """Split estratificado por clase: mismas proporciones en train/dev/test."""
    random.seed(SEED)
    by_label = defaultdict(list)
    for r in rows:
        by_label[r["label"]].append(r)

    train, dev, test = [], [], []
    for items in by_label.values():
        random.shuffle(items)
        n = len(items)
        n_test = int(n * TEST_RATIO)
        n_dev = int(n * DEV_RATIO)
        test += items[:n_test]
        dev += items[n_test:n_test + n_dev]
        train += items[n_test + n_dev:]

    for part in (train, dev, test):
        random.shuffle(part)
    return train, dev, test


def to_docbin(rows, out_path):
    """Serializa a .spacy. Para textcat_multilabel la etiqueta va en doc.cats."""
    nlp = spacy.blank("en")
    db = DocBin()
    for r in rows:
        doc = nlp.make_doc(r["text"])
        # Las DOS labels en TODOS los docs, con 0.0/1.0:
        # si faltan, spaCy no infiere bien el conjunto de etiquetas.
        doc.cats = {lab: float(r["label"] == lab) for lab in LABELS}
        db.add(doc)
    db.to_disk(out_path)


def main():
    rows = []
    for label, path in SOURCES.items():
        rows += read_sentences(path, label)

    if not rows:
        raise SystemExit("No hay oraciones todavía: completá los .txt de data/raw/")

    check_quality(rows)

    train, dev, test = split(rows)
    CORPUS.mkdir(parents=True, exist_ok=True)

    print("\nSplit estratificado:")
    for name, part in (("train", train), ("dev", dev), ("test", test)):
        to_docbin(part, CORPUS / f"{name}.spacy")
        with open(CORPUS / f"{name}.jsonl", "w", encoding="utf-8") as f:
            for r in part:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"  {name:<6} {len(part):>5} -> {name}.spacy")

    print(f"\nListo. Corpus en {CORPUS}")


if __name__ == "__main__":
    main()
