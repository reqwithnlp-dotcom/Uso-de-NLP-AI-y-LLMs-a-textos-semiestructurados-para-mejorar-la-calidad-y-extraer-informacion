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

The project requires the following third-party packages (calculated from imports in the `abstract_words` package):

- pandas
- numpy
- scikit-learn
- xgboost
- gensim
- spacy
- joblib
- sentence-transformers
- fastapi
- pydantic
- uvicorn

Install with pip:

```powershell
pip install pandas numpy scikit-learn xgboost gensim spacy joblib sentence-transformers fastapi pydantic uvicorn
```

or:

```powershell
pip install -r requirements.txt
```

Notes:
- `sentence-transformers` typically requires a deep-learning backend such as `torch`; install `torch` if needed for your platform.
- `sentence-transformers` may also pull `transformers` as a dependency.
- Download recommended spaCy English models:

```powershell
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md
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

## HTTP invocation example

Request (POST) to the `/predict` endpoint:

```http
POST http://localhost:8000/predict
Content-Type: application/json

{
    "text": "Love and freedom are important concepts in philosophy. The dog is sitting next to the table."
}
```

Expected response (JSON):

```json
{
  "results": [
    "love",
    "freedom",
    "important",
    "concepts",
    "philosophy"
  ]
}
```

---

## Unit tests

```powershell
pytest abstract_words/tests -v
```