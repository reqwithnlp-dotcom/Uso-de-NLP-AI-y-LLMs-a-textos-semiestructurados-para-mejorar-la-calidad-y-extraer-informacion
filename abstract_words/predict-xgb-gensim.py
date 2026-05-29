import numpy as np
import joblib
import gensim.downloader as api
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent

# -----------------------------------
# LOAD MODELS
# -----------------------------------

print("Loading FastText embeddings...")

ft = api.load("fasttext-wiki-news-subwords-300")

print("Loading XGBoost model...")

model = joblib.load(BASE_PATH / "xgboost_fasttext_model.joblib")

VECTOR_SIZE = 300

# -----------------------------------
# EMBEDDING FUNCTION
# -----------------------------------

def word_to_vector(word: str):

    word = str(word).lower()

    try:
        return ft[word]
    except KeyError:
        # fallback OOV
        return np.zeros(VECTOR_SIZE)

# -----------------------------------
# PREDICTION FUNCTION
# -----------------------------------

def predict(word: str):

    vector = word_to_vector(word)

    # XGBoost expects 2D input
    prediction = model.predict([vector])[0]

    # convert to abstractness scale (1–5)
    abstractness = 6 - prediction

    return prediction, abstractness

# -----------------------------------
# INTERACTIVE MODE
# -----------------------------------

print("\n=== ABSTRACTNESS PREDICTOR ===")

while True:

    word = input("\nEnter word (or 'exit'): ").strip()

    if word.lower() == "exit":
        break

    concreteness, abstractness = predict(word)

    print("\nRESULT")
    print("----------------------")
    print(f"Word         : {word}")
    print(f"Concreteness : {concreteness:.3f} (1=abstract, 5=concrete)")
    print(f"Abstractness : {abstractness:.3f} (1=concrete, 5=abstract)")