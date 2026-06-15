import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent

# -----------------------------
# CONFIG
# -----------------------------

INPUT_FILE = BASE_PATH / "datasets" / "Concreteness_ratings_Brysbaert_et_al_BRM.txt"

TRAIN_OUTPUT = BASE_PATH / "datasets" / "train.csv"
TEST_OUTPUT = BASE_PATH / "datasets" / "test.csv"

TEST_SIZE = 0.2
RANDOM_STATE = 42

# -----------------------------
# LOAD DATASET
# -----------------------------

print("Loading dataset...")

df = pd.read_csv(INPUT_FILE, sep="\t")

print(f"Total rows: {len(df)}")

# -----------------------------
# BASIC CLEANING
# -----------------------------

# Eliminar filas sin palabra o score
df = df.dropna(subset=["Word", "Conc.M"])

print(f"Rows after cleaning: {len(df)}")

# -----------------------------
# TRAIN / TEST SPLIT
# -----------------------------

train_df, test_df = train_test_split(
    df,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    shuffle=True
)

# -----------------------------
# SAVE FILES
# -----------------------------

train_df.to_csv(TRAIN_OUTPUT, index=False)
test_df.to_csv(TEST_OUTPUT, index=False)

print("\nDone!")
print(f"Train rows: {len(train_df)}")
print(f"Test rows : {len(test_df)}")