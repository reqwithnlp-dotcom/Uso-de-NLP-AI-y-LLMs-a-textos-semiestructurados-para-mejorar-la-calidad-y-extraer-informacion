# Abstract Word Detection - NLP Pipeline

Microservice-oriented NLP pipeline for detecting abstract words in English texts using semantic embeddings and machine learning.

---

# Requirements

- Python 3.10+
- pip
- Internet connection (required the first time embeddings are downloaded)

---

# 1. Create Virtual Environment

## Windows

```powershell
python -m venv venv
```

Activate environment:

```powershell
venv\Scripts\activate
```

---

# 2. Install Dependencies

Install all required libraries:

```powershell
pip install pandas scikit-learn xgboost gensim spacy joblib numpy
```

Download spaCy English model:

```powershell
python -m spacy download en_core_web_sm
```

---

# 4. Execution Order

The scripts must be executed in the following order.

---

## Step 1 — Split Dataset

Splits the original dataset into:
- training dataset
- testing dataset

Run:

```powershell
python split_dataset.py
```

Expected output:

```text
datasets/train.csv
datasets/test.csv
```

---

## Step 2 — Train Model

See the config.json file for service configuration. It specifies the embedding provider and the machine learning model used for abstract word detection.

Possible values: 
```text
embedding: spacy || fasttext || mpnet
model: rf || xgboost
```

Generates semantic embeddings and trains the machine learning model.

Run:

```powershell
python train_model.py
```

Expected output:

```text
fasttext_xgboost.joblib
```

Notes:
- The first execution may take several minutes because embeddings are downloaded and loaded into memory.
- Training metrics such as MAE and R² will be displayed.

---

## Step 3 — Run Abstract Words service

Runs the main service.

Run:

```powershell
python main.py
```

The script will:
1. Receive a text as input
2. Analyze the text linguistically and semantically
3. Detect abstract words
4. Return a unique list of detected abstract words

---

## Unit tests

```powershell
pytest abstract_words/tests -v
```