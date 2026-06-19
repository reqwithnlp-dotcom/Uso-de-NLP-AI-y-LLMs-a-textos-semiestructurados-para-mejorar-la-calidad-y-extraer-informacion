

import pytest
import spacy

try:
    _NLP = spacy.load("en_core_web_sm")
    MODEL_AVAILABLE = True
except OSError:
    _NLP = None
    MODEL_AVAILABLE = False

requires_model = pytest.mark.skipif(
    not MODEL_AVAILABLE,
    reason="Modelo en_core_web_sm no instalado (python -m spacy download en_core_web_sm)",
)


@pytest.fixture(scope="session")
def nlp():
    if _NLP is None:
        pytest.skip("Modelo spaCy no disponible")
    return _NLP


@pytest.fixture(scope="session")
def parse(nlp):
    def _parse(text):
        return next(nlp(text).sents)
    return _parse
