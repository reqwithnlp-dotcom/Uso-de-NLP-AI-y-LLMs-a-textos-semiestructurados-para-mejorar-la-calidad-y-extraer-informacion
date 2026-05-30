import pandas as pd
import joblib
import numpy as np

from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from pathlib import Path

from sentence_transformers import SentenceTransformer

BASE_PATH = Path(__file__).resolve().parent

# -----------------------------------
# LOAD FASTTEXT EMBEDDINGS
# -----------------------------------

print("Loading transformer embeddings...")

embedding_model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
)

def word_to_vector(word):

    embedding = embedding_model.encode(
        word,
        normalize_embeddings=True
    )

    return embedding

# -----------------------------------
# LOAD DATASETS
# -----------------------------------

print("Loading datasets...")

train_df = pd.read_csv(BASE_PATH / "train.csv")
test_df = pd.read_csv(BASE_PATH / "test.csv")

# -----------------------------------
# OPTIONAL CLEANING (igual que antes)
# -----------------------------------

# eliminar filas inválidas
train_df = train_df.dropna(subset=["Word", "Conc.M"])
test_df = test_df.dropna(subset=["Word", "Conc.M"])

# eliminar palabras ambiguas
train_df = train_df[train_df["Conc.SD"] < 1.5]

# mantener palabras conocidas
#train_df = train_df[train_df["Percent_known"] >= 0.8]

print(f"Train rows after cleaning: {len(train_df)}")
print(f"Test rows after cleaning : {len(test_df)}")

# -----------------------------------
# BUILD TRAIN SET
# -----------------------------------

print("Building train embeddings...")

X_train = []
y_train = []

for _, row in train_df.iterrows():

    vec = word_to_vector(row["Word"])

    if np.sum(vec) == 0:
        continue

    X_train.append(vec)
    y_train.append(row["Conc.M"])

# -----------------------------------
# BUILD TEST SET
# -----------------------------------

print("Building test embeddings...")

X_test = []
y_test = []

for _, row in test_df.iterrows():

    vec = word_to_vector(row["Word"])

    if np.sum(vec) == 0:
        continue

    X_test.append(vec)
    y_test.append(row["Conc.M"])

# -----------------------------------
# TRAIN MODEL
# -----------------------------------

print("Training XGBoost...")

model = XGBRegressor(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# -----------------------------------
# EVALUATION
# -----------------------------------

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

joblib.dump(model, BASE_PATH / "xgboost_mpnet_model.joblib")

print("\nModel saved: xgboost_mpnet_model.joblib")