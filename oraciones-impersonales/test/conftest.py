

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


@pytest.fixture(autouse=True)
def _sin_capa2_por_defecto(monkeypatch, tmp_path):
    """Por defecto los tests corren SIN modelo de capa 2, para que el
    resultado no dependa de si hay uno entrenado en model/textcat.
    Los tests que quieran el modelo real lo piden explícitamente."""
    from model import classifier
    monkeypatch.setenv("IMPERSONAL_TEXTCAT_PATH", str(tmp_path / "sin_modelo"))
    classifier.reset()
    yield
    classifier.reset()
