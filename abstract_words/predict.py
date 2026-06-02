import argparse
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent


def main():
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
    from strategies import create_embedding_strategy

    emb_name = (args.embedding or cfg.get("embedding") or "spacy").lower()
    model_arg = args.model or cfg.get("model")
    print(f"Using embedding strategy: {emb_name}")
    embedder = create_embedding_strategy(emb_name)

    # determine model filename
    if model_arg:
        model_path = Path(model_arg)
        print(f"Using model file: {model_path}")
    else:
        # choose default names to keep backward compatibility
        default_map = {
            "spacy": BASE_PATH / "model.joblib",
            "fasttext": BASE_PATH / "xgboost_fasttext_model.joblib",
            "gensim": BASE_PATH / "xgboost_fasttext_model.joblib",
            "mpnet": BASE_PATH / "xgboost_mpnet_model.joblib",
        }
        model_path = default_map.get(emb_name, BASE_PATH / "model.joblib")
        print(f"Using default model file for embedding '{emb_name}': {model_path}")

    if not model_path.exists():
        raise SystemExit(f"Model file not found: {model_path}")

    # load model via model strategy wrapper (joblib used internally)
    import joblib
    loaded = joblib.load(model_path)

    # simple wrapper object to expose predict
    class _SimpleModel:
        def __init__(self, m):
            self.m = m
        def predict(self, X):
            return self.m.predict(X)

    model = _SimpleModel(loaded)

    def predict_word(word: str):
        vec = embedder.embed(word)
        conc = model.predict([vec])[0]
        abstractness = 6 - conc
        return conc, abstractness

    print("\n=== ABSTRACTNESS PREDICTOR ===")
    while True:
        word = input("\nEnter word (or 'exit'): ").strip()
        if word.lower() == "exit":
            break
        conc, abstr = predict_word(word)
        print(f"\nWord: {word}")
        print(f"Concreteness : {conc:.2f}")
        print(f"Abstractness : {abstr:.2f}")


if __name__ == '__main__':
    main()