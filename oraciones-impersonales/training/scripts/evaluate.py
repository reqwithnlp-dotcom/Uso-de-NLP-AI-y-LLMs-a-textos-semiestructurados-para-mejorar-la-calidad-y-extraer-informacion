"""
Evalúa la capa 2 contra el baseline de reglas (capa 1) sobre un split.

Compara tres sistemas sobre las MISMAS oraciones:
    1. capa1     : solo reglas. Las ambiguas no tienen decisión (cuentan
                   como error; se informa la cobertura aparte).
    2. capa2     : solo el clasificador (argmax de los scores, cobertura 100%).
    3. combinado : el pipeline del servicio. Capa 1 en los casos claros y
                   capa 2 (con umbral/margen) en las ambiguas.

La métrica que justifica la capa 2 es la exactitud DENTRO del subconjunto
que la capa 1 deja ambiguo: es exactamente el trabajo que se le delega.

Uso (desde la raíz del servicio):

    # Ajuste de umbral/margen: SIEMPRE sobre dev
    python training/scripts/evaluate.py --split dev --sweep

    # Medición final: test, UNA sola vez, con los valores elegidos en dev
    python training/scripts/evaluate.py --split test --threshold 0.5 --margin 0.2
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SERVICE_ROOT = BASE.parent
sys.path.insert(0, str(SERVICE_ROOT))

import spacy  # noqa: E402

from model.classifier import UNDECIDED, decide  # noqa: E402
from model.detector import _get_nlp, analyze_sentence  # noqa: E402

CORPUS = BASE / "data" / "corpus"
DEFAULT_MODEL = BASE / "output" / "model-best"
LABELS = ("PERSONAL", "IMPERSONAL")


def load_split(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def layer1(rows):
    """Corre la capa 1 sobre la oración ENTERA (como un único span), porque
    las oraciones del corpus ya vienen separadas."""
    nlp = _get_nlp()
    out = []
    for doc in nlp.pipe([r["text"] for r in rows], batch_size=256):
        r = analyze_sentence(doc[:], use_layer2=False)
        out.append(r)
    return out


def metrics(gold, pred):
    """Exactitud, cobertura, P/R/F1 por clase y matriz de confusión.
    `pred` puede contener UNDECIDED: cuenta como error y baja la cobertura."""
    n = len(gold)
    acc = sum(g == p for g, p in zip(gold, pred)) / n if n else 0.0
    cov = sum(p != UNDECIDED for p in pred) / n if n else 0.0
    per = {}
    for lab in LABELS:
        tp = sum(g == lab and p == lab for g, p in zip(gold, pred))
        fp = sum(g != lab and p == lab for g, p in zip(gold, pred))
        fn = sum(g == lab and p != lab for g, p in zip(gold, pred))
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
        per[lab] = {"p": prec, "r": rec, "f1": f1, "support": sum(g == lab for g in gold)}
    macro_f1 = sum(v["f1"] for v in per.values()) / len(LABELS)
    conf = Counter(zip(gold, pred))
    return {"n": n, "accuracy": acc, "coverage": cov, "macro_f1": macro_f1,
            "per_class": per, "confusion": {f"{g}->{p}": c for (g, p), c in sorted(conf.items())}}


def argmax(scores):
    return max(LABELS, key=lambda lab: scores[lab])


def combined(l1, scores, threshold, margin):
    preds = []
    for r, s in zip(l1, scores):
        if not r["ambiguous"]:
            preds.append("IMPERSONAL" if r["impersonal"] else "PERSONAL")
        else:
            preds.append(decide(s, threshold, margin))
    return preds


def print_block(name, m):
    print(f"\n== {name}  (n={m['n']})")
    print(f"   accuracy {m['accuracy']:.3f}   macro-F1 {m['macro_f1']:.3f}   cobertura {m['coverage']:.3f}")
    for lab, v in m["per_class"].items():
        print(f"   {lab:<11} P {v['p']:.3f}  R {v['r']:.3f}  F1 {v['f1']:.3f}  (soporte {v['support']})")
    print("   confusión (gold->pred):", ", ".join(f"{k}: {v}" for k, v in m["confusion"].items()))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--split", default="test", choices=["train", "dev", "test"])
    ap.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    ap.add_argument("--corpus", type=Path, default=CORPUS)
    ap.add_argument("--threshold", type=float, default=0.5)
    ap.add_argument("--margin", type=float, default=0.2)
    ap.add_argument("--sweep", action="store_true", help="Grilla de umbral/margen (usar en dev)")
    ap.add_argument("--json", type=Path, help="Guarda las métricas en este archivo")
    args = ap.parse_args()

    split_path = args.corpus / f"{args.split}.jsonl"
    if not split_path.exists():
        raise SystemExit(f"No existe {split_path}. Corré build_corpus.py")
    if not (args.model / "config.cfg").exists():
        raise SystemExit(f"No hay modelo en {args.model}. Corré spacy train")
    if args.split == "test" and args.sweep:
        print("AVISO: --sweep sobre test contamina la medición final. Usá --split dev.")

    rows = load_split(split_path)
    gold = [r["label"] for r in rows]

    l1 = layer1(rows)
    textcat = spacy.load(args.model)
    scores = [{lab: float(d.cats.get(lab, 0.0)) for lab in LABELS}
              for d in textcat.pipe([r["text"] for r in rows], batch_size=256)]

    p_l1 = [UNDECIDED if r["ambiguous"] else ("IMPERSONAL" if r["impersonal"] else "PERSONAL")
            for r in l1]
    p_l2 = [argmax(s) for s in scores]
    p_comb = combined(l1, scores, args.threshold, args.margin)

    amb_idx = [i for i, r in enumerate(l1) if r["ambiguous"]]
    g_amb = [gold[i] for i in amb_idx]

    results = {
        "split": args.split, "model": str(args.model),
        "threshold": args.threshold, "margin": args.margin,
        "capa1": metrics(gold, p_l1),
        "capa2": metrics(gold, p_l2),
        "combinado": metrics(gold, p_comb),
        "ambiguas_capa1": {
            "n": len(amb_idx),
            "pct": len(amb_idx) / len(rows) if rows else 0.0,
            "capa2_argmax": metrics(g_amb, [p_l2[i] for i in amb_idx]) if amb_idx else None,
            "capa2_umbral": metrics(g_amb, [p_comb[i] for i in amb_idx]) if amb_idx else None,
        },
    }

    print(f"Split: {args.split} ({len(rows)} oraciones)   modelo: {args.model}")
    print_block("CAPA 1 sola (reglas)", results["capa1"])
    print_block("CAPA 2 sola (argmax)", results["capa2"])
    print_block(f"COMBINADO (umbral {args.threshold}, margen {args.margin})", results["combinado"])

    amb = results["ambiguas_capa1"]
    print(f"\n== Subconjunto AMBIGUO de capa 1: {amb['n']} oraciones ({100 * amb['pct']:.1f}%)")
    if amb["n"]:
        a, u = amb["capa2_argmax"], amb["capa2_umbral"]
        print(f"   capa 2 argmax : accuracy {a['accuracy']:.3f}")
        print(f"   capa 2 umbral : accuracy {u['accuracy']:.3f}  cobertura {u['coverage']:.3f}")

    if args.sweep:
        print("\n== Barrido umbral/margen (combinado)")
        print("   umbral margen  accuracy  cobertura  macro-F1")
        for th in (0.5, 0.6, 0.7, 0.8):
            for mg in (0.0, 0.1, 0.2, 0.3, 0.5):
                m = metrics(gold, combined(l1, scores, th, mg))
                print(f"   {th:<6} {mg:<6}  {m['accuracy']:.3f}     {m['coverage']:.3f}      {m['macro_f1']:.3f}")

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nMétricas guardadas en {args.json}")


if __name__ == "__main__":
    main()
