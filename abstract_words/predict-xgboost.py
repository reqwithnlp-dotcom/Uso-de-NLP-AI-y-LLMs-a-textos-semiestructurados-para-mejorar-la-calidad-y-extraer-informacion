import spacy
import joblib

# -----------------------------------
# LOAD MODELS
# -----------------------------------

print("Loading spaCy model...")

nlp = spacy.load("en_core_web_md")

print("Loading XGBoost model...")

model = joblib.load("xgboost_model.joblib")

# -----------------------------------
# FEATURE FUNCTION
# -----------------------------------

def word_to_vector(word: str):

    doc = nlp(str(word).lower())
    return doc.vector

# -----------------------------------
# PREDICT FUNCTION
# -----------------------------------

def predict(word: str):

    vector = word_to_vector(word)

    concreteness = model.predict([vector])[0]

    abstractness = 6 - concreteness  # escala 1–5 invertida

    return concreteness, abstractness

# -----------------------------------
# INTERACTIVE MODE
# -----------------------------------

print("\n=== ABSTRACTNESS PREDICTOR ===")

while True:

    word = input("\nEnter word (or 'exit'): ").strip()

    if word.lower() == "exit":
        break

    concreteness, abstractness = predict(word)

    print("\nRESULT:")
    print(f"Word          : {word}")
    print(f"Concreteness  : {concreteness:.2f} (1=abstract, 5=concrete)")
    print(f"Abstractness  : {abstractness:.2f} (1=concrete, 5=abstract)")