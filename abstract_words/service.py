import argparse
from pathlib import Path

import spacy

BASE_PATH = Path(__file__).resolve().parent

class Context:
    model = None
    embedder = None
    nlp = None

# palabras gramaticales que no aportan abstracción
EXCLUDED_POS = {
    "DET",
    "PRON",
    "ADP",
    "CCONJ",
    "SCONJ",
    "PART",
    "AUX",
    "PUNCT",
    "NUM",
    "SPACE"
}

# =========================================
# INIT FUNCTION
# =========================================
def setup():    
    parser = argparse.ArgumentParser()
    parser.add_argument("--embedding", default=None, help="Embedding strategy: spacy|mpnet|fasttext")
    parser.add_argument("--model", default=None, help="Model strategy or filename. If omitted, inferred from embedding")
    parser.add_argument("--config", default=str(BASE_PATH / "config.json"), help="Path to JSON config file")
    args = parser.parse_args()

    # load config if present
    import json
    config_path = Path(args.config)
    cfg = {}
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as fh:
                cfg = json.load(fh)
        except Exception:
            print(f"Warning: failed to read config {config_path}, ignoring")

    import sys
    sys.path.insert(0, str(BASE_PATH))
    from strategies import create_embedding_strategy, get_default_model_path

    emb_name = (args.embedding or cfg.get("embedding") or "spacy").lower()
    model_arg = args.model or cfg.get("model")
    print(f"Using embedding strategy: {emb_name}")
    Context.embedder = create_embedding_strategy(emb_name)

    # determine model filename from strategy helper
    file_model_path = get_default_model_path(BASE_PATH, model_arg, emb_name)

    if not file_model_path.exists():
        raise SystemExit(f"Model file not found: {file_model_path}")

    # load model via model strategy wrapper (joblib used internally)
    import joblib
    loaded = joblib.load(file_model_path)

    # simple wrapper object to expose predict
    class _SimpleModel:
        def __init__(self, m):
            self.m = m
        def predict(self, X):
            return self.m.predict(X)

    Context.model = _SimpleModel(loaded)

    print("Loading spaCy...")
    Context.nlp = spacy.load("en_core_web_sm")

# =========================================
# EMBEDDING FUNCTION
# =========================================

def word_to_vector(word: str):
    return Context.embedder.embed(word)

# =========================================
# ABSTRACTNESS PREDICTION
# =========================================

def predict_word(word: str):
    vec = Context.embedder.embed(word)
    conc = Context.model.predict([vec])[0]
    abstractness = 6 - conc
    return abstractness


# =========================================
# MAIN FUNCTION
# =========================================

def extract_abstract_words(text: str, threshold: float = 3.0):

    doc = Context.nlp(text)

    results = []

    # para evitar duplicados
    processed_words = set()

    for token in doc:

        # ignorar basura
        if token.is_stop:
            continue

        if token.is_punct:
            continue

        if token.pos_ in EXCLUDED_POS:
            continue

        # usar lema
        lemma = token.lemma_.lower().strip()
        word = token.text.lower().strip()

        # ignorar cosas raras
        if len(lemma) < 2:
            continue

        if not lemma.isalpha():
            continue

        # evitar repetidos
        if word in processed_words:
            continue

        processed_words.add(word)

        # score
        abstractness = predict_word(lemma)

        if abstractness is None:
            continue

        # aplicar threshold
        if abstractness >= threshold:

            results.append(word)

    return results