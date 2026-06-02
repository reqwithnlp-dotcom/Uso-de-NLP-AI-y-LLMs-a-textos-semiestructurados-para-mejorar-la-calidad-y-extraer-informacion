import argparse
from pathlib import Path
import pandas as pd
import numpy as np

BASE_PATH = Path(__file__).resolve().parent


def load_datasets():
    train_df = pd.read_csv(BASE_PATH / "train.csv")
    test_df = pd.read_csv(BASE_PATH / "test.csv")

    train_df = train_df.dropna(subset=["Word", "Conc.M"])
    test_df = test_df.dropna(subset=["Word", "Conc.M"])

    train_df = train_df[train_df["Conc.SD"] < 1.5]

    print(f"Train rows after cleaning: {len(train_df)}")
    print(f"Test rows after cleaning : {len(test_df)}")

    return train_df, test_df


def build_embeddings(df, embedder):
    X = []
    y = []

    for _, row in df.iterrows():
        vec = embedder.embed(row["Word"])
        if np.sum(vec) == 0:
            continue
        X.append(vec)
        y.append(row["Conc.M"])

    return X, y


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--embedding", default=None, help="Embedding strategy: spacy|mpnet|fasttext")
    parser.add_argument("--model", default=None, help="Model strategy: rf|xgboost")
    parser.add_argument("--save", default=None, help="Filename to save model")
    parser.add_argument("--config", default=str(BASE_PATH / "config.json"), help="Path to JSON config file")
    args = parser.parse_args()

    # load config (JSON, no extra deps)
    import json
    config_path = Path(args.config)
    cfg = {}
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as fh:
                cfg = json.load(fh)
        except Exception:
            print(f"Warning: failed to read config {config_path}, ignoring")

    # CLI args take precedence over config values
    emb_arg = args.embedding or cfg.get("embedding") or "spacy"
    model_arg = args.model or cfg.get("model") or "rf"
    save_arg = args.save if args.save is not None else cfg.get("save")

    # lazy imports to reduce startup cost when not needed
    import sys
    sys.path.insert(0, str(BASE_PATH))
    from strategies import create_embedding_strategy, create_ml_model_strategy

    print("Loading datasets...")
    train_df, test_df = load_datasets()

    emb_name = emb_arg.lower()
    print(f"Using embedding strategy: {emb_name}")
    embedder = create_embedding_strategy(emb_name)

    print("Building embeddings for train/test...")
    X_train, y_train = build_embeddings(train_df, embedder)
    X_test, y_test = build_embeddings(test_df, embedder)

    print(f"Using ML model strategy: {model_arg.lower()}")
    model = create_ml_model_strategy(model_arg)
    if model_arg.lower() in ("rf", "randomforest"):
        default_save = BASE_PATH / "model.joblib"
    else:
        save_map = {
            "spacy": BASE_PATH / "xgboost_model.joblib",
            "fasttext": BASE_PATH / "xgboost_fasttext_model.joblib",
            "gensim": BASE_PATH / "xgboost_fasttext_model.joblib",
            "mpnet": BASE_PATH / "xgboost_mpnet_model.joblib",
        }
        default_save = save_map.get(emb_name, BASE_PATH / "xgboost_model.joblib")

    print("Training model...")
    model.fit(X_train, y_train)

    print("Evaluating model...")
    preds = model.predict(X_test)

    from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score, precision_score, recall_score, f1_score

    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    THRESHOLD = 3
    y_test_binary = [1 if y > THRESHOLD else 0 for y in y_test]
    pred_binary = [1 if y > THRESHOLD else 0 for y in preds]

    accuracy = accuracy_score(y_test_binary, pred_binary)
    precision = precision_score(y_test_binary, pred_binary)
    recall = recall_score(y_test_binary, pred_binary)
    f1 = f1_score(y_test_binary, pred_binary)

    print("\nRESULTS")
    print("--------------------")
    print(f"MAE: {mae:.4f}")
    print(f"R2 : {r2:.4f}")
    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")

    save_path = Path(save_arg) if save_arg else default_save
    print(f"Saving model to {save_path}")
    model.save(save_path)


if __name__ == '__main__':
    main()