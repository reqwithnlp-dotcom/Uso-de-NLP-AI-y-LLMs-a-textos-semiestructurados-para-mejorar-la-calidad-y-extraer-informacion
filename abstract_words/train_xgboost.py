import pandas as pd
import spacy
import joblib
import numpy as np

from xgboost import XGBRegressor

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

# -----------------------------------
# LOAD SPACY MODEL
# -----------------------------------

print("Loading spaCy model...")

nlp = spacy.load("en_core_web_md")

# -----------------------------------
# LOAD DATASETS
# -----------------------------------

print("Loading datasets...")

train_df = pd.read_csv("train.csv")
test_df = pd.read_csv("test.csv")

# -----------------------------------
# EXTRA CLEANING
# -----------------------------------

# eliminar filas inválidas
train_df = train_df.dropna(subset=["Word", "Conc.M"])
test_df = test_df.dropna(subset=["Word", "Conc.M"])

# eliminar palabras ambiguas
train_df = train_df[train_df["Conc.SD"] < 1.2]
test_df = test_df[test_df["Conc.SD"] < 1.2]

# mantener palabras conocidas
train_df = train_df[train_df["Percent_known"] >= 0.9]
test_df = test_df[test_df["Percent_known"] >= 0.9]

print(f"Train rows after cleaning: {len(train_df)}")
print(f"Test rows after cleaning : {len(test_df)}")

# -----------------------------------
# VECTOR FUNCTION
# -----------------------------------

def word_to_vector(word):

    doc = nlp(str(word).lower())

    return doc.vector

# -----------------------------------
# BUILD TRAIN SET
# -----------------------------------

print("Generating train embeddings...")

X_train = []
y_train = []

for _, row in train_df.iterrows():

    word = row["Word"]
    conc = row["Conc.M"]

    vector = word_to_vector(word)

    # ignorar vectores vacíos
    if np.sum(vector) == 0:
        continue

    X_train.append(vector)
    y_train.append(conc)

# -----------------------------------
# BUILD TEST SET
# -----------------------------------

print("Generating test embeddings...")

X_test = []
y_test = []

for _, row in test_df.iterrows():

    word = row["Word"]
    conc = row["Conc.M"]

    vector = word_to_vector(word)

    if np.sum(vector) == 0:
        continue

    X_test.append(vector)
    y_test.append(conc)

# -----------------------------------
# TRAIN XGBOOST
# -----------------------------------

print("Training XGBoost model...")

model = XGBRegressor(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective='reg:squarederror',
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# -----------------------------------
# EVALUATION
# -----------------------------------

print("Evaluating model...")

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

# -----------------------------------
# CONVERT TO BINARY CLASSES
# -----------------------------------

THRESHOLD = 3

y_test_binary = [
    1 if y > THRESHOLD else 0
    for y in y_test
]

pred_binary = [
    1 if y > THRESHOLD else 0
    for y in predictions
]

# -----------------------------------
# METRICS
# -----------------------------------

accuracy = accuracy_score(
    y_test_binary,
    pred_binary
)

precision = precision_score(
    y_test_binary,
    pred_binary
)

recall = recall_score(
    y_test_binary,
    pred_binary
)

f1 = f1_score(
    y_test_binary,
    pred_binary
)

print("\nSpacy embeddings and XGBoost")
print("\nRESULTS")
print("--------------------")
print(f"MAE: {mae:.4f}")
print(f"R2 : {r2:.4f}")
print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")

# -----------------------------------
# SAVE MODEL
# -----------------------------------

print("\nSaving model...")

joblib.dump(model, "xgboost_model.joblib")

print("Model saved as xgboost_model.joblib")

# -----------------------------------
# SAMPLE PREDICTIONS
# -----------------------------------

print("\nSAMPLE PREDICTIONS")
print("--------------------")

sample_words = [
    "love",
    "freedom",
    "table",
    "dog",
    "philosophy",
    "happiness",
    "mindfulness",
    "cybersecurity"
]

for word in sample_words:

    vector = word_to_vector(word)

    prediction = model.predict([vector])[0]

    abstractness = 6 - prediction

    print(
        f"{word:15} "
        f"concreteness={prediction:.2f} "
        f"abstractness={abstractness:.2f}"
    )