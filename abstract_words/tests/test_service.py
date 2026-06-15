import spacy
from abstract_words.service import Context, extract_abstract_words


try:
    SPACY_NLP = spacy.load("en_core_web_sm")
except OSError:
    SPACY_NLP = spacy.blank("en")


class DummyEmbedder:
    def embed(self, word: str):
        return word


class DummyModel:
    def __init__(self, predictions):
        self.predictions = predictions

    def predict(self, X):
        return [self.predictions.get(X[0], 4)]


def test_extract_abstract_words_with_spacy_orchestration(monkeypatch):
    monkeypatch.setattr(Context, "nlp", SPACY_NLP)
    monkeypatch.setattr(Context, "embedder", DummyEmbedder())
    monkeypatch.setattr(Context, "model", DummyModel({"requirement": 1, "analysis": 1, "quality": 5}))

    result = extract_abstract_words("Requirement analysis improves quality.", threshold=3.0)

    assert result == ["requirement", "analysis"]


def test_extract_abstract_words_filters_stop_pos_and_duplicates(monkeypatch):
    monkeypatch.setattr(Context, "nlp", SPACY_NLP)
    monkeypatch.setattr(Context, "embedder", DummyEmbedder())
    monkeypatch.setattr(Context, "model", DummyModel({"happiness": 2, "fact": 5}))

    result = extract_abstract_words("Happiness happiness and is 123 fact", threshold=3.0)

    assert result == ["happiness"]


def test_extract_abstract_words_respects_threshold(monkeypatch):
    monkeypatch.setattr(Context, "nlp", SPACY_NLP)
    monkeypatch.setattr(Context, "embedder", DummyEmbedder())
    monkeypatch.setattr(Context, "model", DummyModel({"dream": 4}))

    result = extract_abstract_words("dream", threshold=3.0)

    assert result == []


def test_extract_abstract_words_case_1(monkeypatch):
    monkeypatch.setattr(Context, "nlp", SPACY_NLP)
    monkeypatch.setattr(Context, "embedder", DummyEmbedder())

    monkeypatch.setattr(
        Context,
        "model",
        DummyModel({
            "the": 5,
            "most": 1,
            "important": 1,
            "thing": 5,
            "is": 5,
            "to": 5,
            "keep": 5,
            "our": 5,
            "calm": 1,
        }),
    )

    result = extract_abstract_words(
        "The most important thing is to keep our calm.",
        threshold=3.0,
    )

    assert result == ["important", "calm"]


def test_extract_abstract_words_case_2(monkeypatch):
    monkeypatch.setattr(Context, "nlp", SPACY_NLP)
    monkeypatch.setattr(Context, "embedder", DummyEmbedder())

    monkeypatch.setattr(
        Context,
        "model",
        DummyModel({
            "kindness": 1,
            "and": 5,
            "generosity": 1,
            "build": 5,
            "a": 5,
            "community": 1,
        }),
    )

    result = extract_abstract_words(
        "Kindness and generosity build a community.",
        threshold=3.0,
    )

    assert result == ["kindness", "generosity", "community"]


def test_extract_abstract_words_case_3(monkeypatch):
    monkeypatch.setattr(Context, "nlp", SPACY_NLP)
    monkeypatch.setattr(Context, "embedder", DummyEmbedder())

    monkeypatch.setattr(
        Context,
        "model",
        DummyModel({
            "loving": 1,
            "with": 5,
            "love": 1,
            "and": 1,
            "in": 1,
            "a": 1,
            "way": 5,
        }),
    )

    result = extract_abstract_words(
        "Loving with love and loving in a loving way.",
        threshold=3.0,
    )

    assert result == ["loving", "love"]