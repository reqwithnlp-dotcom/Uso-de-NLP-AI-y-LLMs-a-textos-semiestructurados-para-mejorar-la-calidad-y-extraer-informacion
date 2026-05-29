import spacy
import joblib
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent

# -----------------------------------
# LOAD SPACY
# -----------------------------------

print("Loading spaCy...")

nlp = spacy.load("en_core_web_md")

# -----------------------------------
# LOAD MODEL
# -----------------------------------

print("Loading model...")

model = joblib.load(BASE_PATH / "model.joblib")

# -----------------------------------
# PREDICT FUNCTION
# -----------------------------------

def predict_word(word):

    doc = nlp(word)

    vector = doc.vector

    concreteness = model.predict([vector])[0]

    abstractness = 6 - concreteness

    return concreteness, abstractness

# -----------------------------------
# LOOP
# -----------------------------------

while True:

    word = input("\nEnter word (or exit): ")

    if word.lower() == "exit":
        break

    concreteness, abstractness = predict_word(word)

    print(f"\nWord: {word}")
    print(f"Concreteness : {concreteness:.2f}")
    print(f"Abstractness : {abstractness:.2f}")