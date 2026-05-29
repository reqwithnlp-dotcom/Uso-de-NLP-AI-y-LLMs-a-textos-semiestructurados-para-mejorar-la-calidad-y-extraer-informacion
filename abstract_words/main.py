import numpy as np
import joblib
import gensim.downloader as api
import spacy

from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent

# =========================================
# LOAD NLP + MODELS
# =========================================

print("Loading spaCy...")

nlp = spacy.load("en_core_web_sm")

print("Loading FastText embeddings...")

ft = api.load("fasttext-wiki-news-subwords-300")

print("Loading XGBoost model...")

model = joblib.load(BASE_PATH / "xgboost_fasttext_model.joblib")

VECTOR_SIZE = 300

# =========================================
# CONFIG
# =========================================

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
# EMBEDDING FUNCTION
# =========================================

def word_to_vector(word: str):

    word = str(word).lower()

    try:
        return ft[word]

    except KeyError:
        return np.zeros(VECTOR_SIZE)

# =========================================
# ABSTRACTNESS PREDICTION
# =========================================

def predict_abstractness(word: str):

    vector = word_to_vector(word)

    # ignorar embeddings vacíos
    if np.sum(vector) == 0:
        return None

    concreteness = model.predict([vector])[0]

    # convertir escala
    abstractness = 6 - concreteness

    return round(float(abstractness), 3)

# =========================================
# MAIN PIPELINE
# =========================================

def extract_abstract_words(text: str, threshold: float = 3.0):

    doc = nlp(text)

    results = []

    # para evitar duplicados
    processed_lemmas = set()

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

        # ignorar cosas raras
        if len(lemma) < 2:
            continue

        if not lemma.isalpha():
            continue

        # evitar repetidos
        if lemma in processed_lemmas:
            continue

        processed_lemmas.add(lemma)

        # score
        abstractness = predict_abstractness(lemma)

        if abstractness is None:
            continue

        # aplicar threshold
        if abstractness >= threshold:

            results.append({
                "word": token.text,
                "lemma": lemma,
                "pos": token.pos_,
                "abstractness": abstractness
            })

    # ordenar por abstracción descendente
    results.sort(
        key=lambda x: x["abstractness"],
        reverse=True
    )

    return results

# =========================================
# INTERACTIVE TEST
# =========================================

if __name__ == "__main__":

    print("\n=== ABSTRACT WORD EXTRACTOR ===")

    while True:

        text = input("\nEnter text (or 'exit'): ")

        if text.lower() == "exit":
            break

        threshold_input = input(
            "Abstractness threshold (1-5, default=3): "
        ).strip()

        threshold = 3.4

        if threshold_input:
            threshold = float(threshold_input)

        results = extract_abstract_words(
            text=text,
            threshold=threshold
        )

        print("\nRESULTS")
        print("----------------------------------")

        if not results:
            print("No abstract words found.")

        for item in results:

            print(
                f"{item['word']:15} "
                f"lemma={item['lemma']:15} "
                f"pos={item['pos']:6} "
                f"abstractness={item['abstractness']}"
            )