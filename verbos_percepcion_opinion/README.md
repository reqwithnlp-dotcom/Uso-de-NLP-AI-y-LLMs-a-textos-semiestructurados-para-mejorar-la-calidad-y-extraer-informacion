# verbos_percepcion_opinion

Small API to detect perception and opinion verbs in English text.

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt` (install inside a virtual environment)
- spaCy English model: `en_core_web_sm` (see notes)

## Installation

Create and activate a virtual environment, then:

Always activate the virtual environment before running the API or the tests.

```bash
python -m pip install -r requirements.txt
# if you use spaCy for the first time:
python -m spacy download en_core_web_sm
```

## Run the API (development)

```bash
uvicorn perception_opinion_api:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Endpoints

- `POST /perception-opinion` — expects JSON with the shape:

```json
{ "text": "I think this is fine." }
```

Response (200) — example:

```json
{
  "opinion_perception": ["think"],
  "others": ["I", "this", "is", "fine"]
}
```

Common errors:
- 400: when `text` is empty.
- 500: internal error while processing the text.

## Tests

Tests use `unittest` and `fastapi.testclient`.

```bash
python -m unittest api_test.py
python -m unittest service_test.py
```

## Notes

- If you don't need spaCy for quick tests (e.g. using mocks), you can run tests without downloading the model, but to run the API fully it's recommended to install `en_core_web_sm`.
