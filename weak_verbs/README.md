# weak_verbs

Small API to detect weak verbs in English text.

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`.
- spaCy English model: `en_core_web_sm`.

## Installation

Create and activate a virtual environment, then install the dependencies:

```bash
python -m pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

If the spaCy model is not installed, the application will not start correctly.

## Run the API

Start the service in development mode with:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Endpoint

- `POST /weak_verbs`

Request body:

```json
{ "text": "She made a decision." }
```

Successful response example:

```json
["made"]
```

The endpoint returns a plain list with the weak verbs found in the text.

Common errors:

- `400`: when `text` is empty.
- `500`: internal error while processing the text.

## Tests

The project uses `unittest` and `fastapi.testclient`.

Run the tests with:

```bash
python tests/api_test.py
```

## Notes

- Weak verbs are detected using spaCy lemmatization and POS tagging.
- The current weak verb list includes common forms such as `do`, `make`, `have`, `get`, `take`, `give`, `go`, `run`, `keep`, `play`, `put`, `set`, and `be`.
- The service also detect and exclude those weaks verbs that are phrasal verbs.
