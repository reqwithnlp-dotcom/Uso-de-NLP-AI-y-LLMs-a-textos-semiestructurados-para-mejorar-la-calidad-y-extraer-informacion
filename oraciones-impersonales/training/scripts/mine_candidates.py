"""
Mina oraciones candidatas para el corpus (enfoque semiautomático).

Fuentes:
    - Treebanks UD en inglés (.conllu) en training/data/external/
      (EWT y GUM). UD anota el "it"/"there" vacío como `expl`: eso da una
      etiqueta *silver* hecha por humanos.
    - Opcional: archivos .txt / .json con texto libre (--extra).

Para cada candidata corre la capa 1 (model.detector.analyze_sentence) y
propone una etiqueta. El resultado es un CSV para revisar a mano:

    training/data/review/candidates.csv

Columna a completar por quien revisa: `final_label`
(PERSONAL / IMPERSONAL / UNCLEAR; vacío = descartar).
Después: python training/scripts/import_reviewed.py

Uso (desde la raíz del servicio, la carpeta que contiene main.py):

    python training/scripts/mine_candidates.py
    python training/scripts/mine_candidates.py --extra ../../reviews_games.json
"""

import argparse
import csv
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]          # .../training
SERVICE_ROOT = BASE.parent                          # carpeta con main.py
sys.path.insert(0, str(SERVICE_ROOT))

from model.detector import _get_nlp, analyze_sentence  # noqa: E402

EXTERNAL = BASE / "data" / "external"
RAW = BASE / "data" / "raw"
OUT = BASE / "data" / "review" / "candidates.csv"

SEED = 42

# Señal UD de cada oración (ver ud_signal()).
#   EXPL_ROOT : it/there expletivo colgando de la raíz -> IMPERSONAL (silver)
#   EXPL_OTHER: expletivo de la raíz que no es sujeto (objeto, modismo)
#                                                       -> lo decide el humano
#   EXPL_SUB  : expletivo solo en una subordinada      -> lo decide el humano
#   IT_REF    : "it" referencial sujeto de la raíz     -> PERSONAL (hard negative)
#   SUBJ      : otro sujeto explícito de la raíz       -> PERSONAL (silver)
#   NONE      : sin señal UD (texto libre)             -> propone la capa 1
SILVER = {"EXPL_ROOT": "IMPERSONAL", "IT_REF": "PERSONAL", "SUBJ": "PERSONAL"}

# Cuántas oraciones tomar como máximo de cada grupo.
DEFAULT_CAPS = {
    "EXPL_ROOT_there": 250,
    "EXPL_ROOT_it": 350,
    "IT_REF": 400,
    "EXPL_SUB": 120,
    "EXPL_OTHER": 60,
    "SUBJ": 250,
    "NONE": 300,
}

MIN_WORDS, MAX_WORDS = 4, 30
_BAD = re.compile(r"https?://|www\.|@|\.com\b|\|")

FIELDS = [
    "id", "source", "text", "ud_signal",
    "l1_personal", "l1_impersonal", "l1_ambiguous", "l1_type", "l1_personal_type",
    "proposed_label", "conflict", "final_label", "notes",
]


# ---------------------------------------------------------------------------
# Lectura de fuentes
# ---------------------------------------------------------------------------

def read_conllu(path):
    """Itera (texto, tokens) de un .conllu. Cada token: dict id/form/head/deprel."""
    text, toks = None, []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("# text ="):
                text = line.split("=", 1)[1].strip()
            elif not line:
                if text and toks:
                    yield text, toks
                text, toks = None, []
            elif not line.startswith("#"):
                cols = line.split("\t")
                if len(cols) < 8 or not cols[0].isdigit():  # multiword / nodos vacíos
                    continue
                toks.append({
                    "id": int(cols[0]), "form": cols[1],
                    "head": int(cols[6]) if cols[6].isdigit() else -1,
                    "deprel": cols[7],
                })
    if text and toks:
        yield text, toks


def ud_signal(toks):
    """Clasifica la oración según la anotación UD (ver SILVER)."""
    root = next((t for t in toks if t["deprel"] == "root"), None)
    if root is None:
        return None
    expls = [t for t in toks
             if t["deprel"] == "expl" and t["form"].lower() in ("it", "there")]
    subj = next((t for t in toks
                 if t["head"] == root["id"] and t["deprel"].startswith("nsubj")), None)
    root_expls = [t for t in expls if t["head"] == root["id"]]
    if root_expls:
        # Sujeto vacío = expletivo ANTES del verbo y ningún sujeto real antes
        # del verbo. OJO: en UD el pivote existencial es `nsubj` ("There are
        # many REASONS") y la cláusula extrapuesta es `csubj` ("It is important
        # TO MONITOR"), pero ambos van DESPUÉS del verbo.
        # Descarta el expletivo objeto ("I leave it to you to...", "Rumor had
        # it...") y modismos con sujeto antepuesto ("There you go...").
        pre_subj = [t for t in toks if t["head"] == root["id"]
                    and t["deprel"].startswith(("nsubj", "csubj")) and t["id"] < root["id"]]
        if not pre_subj and any(t["id"] < root["id"] for t in root_expls):
            return "EXPL_ROOT"
        return "EXPL_OTHER"
    if expls:
        return "EXPL_SUB"
    if subj is None:
        return None  # imperativos, fragmentos: no aportan señal fiable
    return "IT_REF" if subj["form"].lower() == "it" else "SUBJ"


def expl_word(toks):
    for t in toks:
        if t["deprel"] == "expl" and t["form"].lower() in ("it", "there"):
            return t["form"].lower()
    return ""


def read_extra(path):
    """Texto libre: .txt (todo el archivo) o .json (lista de strings u objetos)."""
    raw = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() == ".json":
        data = json.loads(raw)
        items = data if isinstance(data, list) else list(data.values())
        chunks = []
        for it in items:
            if isinstance(it, str):
                chunks.append(it)
            elif isinstance(it, dict):
                chunks += [v for v in it.values() if isinstance(v, str) and len(v.split()) > 2]
        return chunks
    return [raw]


def clean_ok(text):
    n = len(text.split())
    return (MIN_WORDS <= n <= MAX_WORDS and text[:1].isupper()
            and text[-1:] in ".!?" and not _BAD.search(text))


def already_in_corpus():
    seen = set()
    for p in RAW.glob("*.txt"):
        for line in p.read_text(encoding="utf-8-sig").splitlines():
            s = line.strip()
            if s and not s.startswith("#"):
                seen.add(s.lower())
    return seen


# ---------------------------------------------------------------------------
# Armado de candidatas
# ---------------------------------------------------------------------------

def collect_ud(caps, rng):
    files = sorted(EXTERNAL.glob("*.conllu"))
    if not files:
        print(f"AVISO: no hay .conllu en {EXTERNAL} (ver training/README.md)")
    buckets = defaultdict(list)
    for path in files:
        for text, toks in read_conllu(path):
            if not clean_ok(text):
                continue
            sig = ud_signal(toks)
            if sig is None:
                continue
            key = f"EXPL_ROOT_{expl_word(toks)}" if sig == "EXPL_ROOT" else sig
            if key in caps:
                buckets[key].append({"source": path.name, "text": text, "ud_signal": sig})
    picked = []
    for key, items in buckets.items():
        rng.shuffle(items)
        picked += items[:caps[key]]
        print(f"  UD {key:<16} disponibles {len(items):>5}  tomadas {min(len(items), caps[key]):>4}")
    return picked


def collect_extra(paths, nlp, cap, rng):
    picked = []
    for p in paths:
        for chunk in read_extra(Path(p)):
            for sent in nlp(chunk).sents:
                t = sent.text.strip()
                if clean_ok(t):
                    picked.append({"source": Path(p).name, "text": t, "ud_signal": "NONE"})
    rng.shuffle(picked)
    if paths:
        print(f"  extra             disponibles {len(picked):>5}  tomadas {min(len(picked), cap):>4}")
    return picked[:cap]


def layer1_decision(r):
    if r["ambiguous"]:
        return ""
    return "IMPERSONAL" if r["impersonal"] else "PERSONAL"


def annotate(cands, nlp):
    """Corre la capa 1 como lo hace el servicio (oración por oración).
    Descarta las que spaCy parte en más de una oración: no serían comparables."""
    rows = []
    texts = [c["text"] for c in cands]
    for c, doc in zip(cands, nlp.pipe(texts, batch_size=256)):
        sents = list(doc.sents)
        if len(sents) != 1:
            continue
        r = analyze_sentence(sents[0], use_layer2=False)
        silver = SILVER.get(c["ud_signal"], "")
        l1 = layer1_decision(r)
        rows.append({
            **c,
            "l1_personal": r["personal"],
            "l1_impersonal": r["impersonal"],
            "l1_ambiguous": r["ambiguous"],
            "l1_type": r["type"],
            "l1_personal_type": r["personal_type"] or "",
            # La anotación UD es humana: tiene prioridad sobre las reglas.
            "proposed_label": silver or l1,
            "conflict": bool(silver and l1 and silver != l1),
            "final_label": "",
            "notes": "",
        })
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--extra", nargs="*", default=[], help=".txt/.json con texto libre en inglés")
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--delimiter", default=";",
                    help="Separador del CSV (';' abre bien en Excel en español)")
    ap.add_argument("--scale", type=float, default=1.0,
                    help="Multiplica todos los topes por grupo (ej. 0.5 para una tanda chica)")
    args = ap.parse_args()

    rng = random.Random(SEED)
    caps = {k: int(v * args.scale) for k, v in DEFAULT_CAPS.items()}
    nlp = _get_nlp()

    print("Recolectando candidatas:")
    cands = collect_ud(caps, rng) + collect_extra(args.extra, nlp, caps["NONE"], rng)

    seen = already_in_corpus()
    uniq, keys = [], set()
    for c in cands:
        k = c["text"].lower()
        if k not in seen and k not in keys:
            keys.add(k)
            uniq.append(c)

    print(f"\nCorriendo capa 1 sobre {len(uniq)} oraciones...")
    rows = annotate(uniq, nlp)

    # Orden de revisión: primero conflictos, luego ambiguas, luego el resto.
    rows.sort(key=lambda r: (not r["conflict"], not r["l1_ambiguous"], r["ud_signal"]))
    for i, r in enumerate(rows, 1):
        r["id"] = i

    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.exists():
        print(f"AVISO: se sobrescribe {args.out}")
    with open(args.out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, delimiter=args.delimiter)
        w.writeheader()
        w.writerows(rows)

    print(f"\n{len(rows)} candidatas -> {args.out}")
    print(f"  conflictos capa1 vs UD : {sum(r['conflict'] for r in rows)}")
    print(f"  ambiguas en capa 1     : {sum(r['l1_ambiguous'] for r in rows)}")
    print(f"  propuestas             : {dict(Counter(r['proposed_label'] or '(vacía)' for r in rows))}")
    print("\nCompletá la columna final_label y corré import_reviewed.py")


if __name__ == "__main__":
    main()
