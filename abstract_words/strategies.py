import abc
import numpy as np
from pathlib import Path
import joblib


class EmbeddingStrategy(abc.ABC):
    @abc.abstractmethod
    def embed(self, text: str):
        raise NotImplementedError()


class SpacyEmbedding(EmbeddingStrategy):
    def __init__(self, nlp):
        self.nlp = nlp

    def embed(self, text: str):
        return self.nlp(str(text)).vector


class GensimFastTextEmbedding(EmbeddingStrategy):
    def __init__(self, ft_model, vector_size=300):
        self.ft = ft_model
        self.vector_size = vector_size

    def embed(self, text: str):
        key = str(text).lower()
        try:
            return self.ft[key]
        except Exception:
            return np.zeros(self.vector_size)


class SentenceTransformerEmbedding(EmbeddingStrategy):
    def __init__(self, model):
        self.model = model

    def embed(self, text: str):
        emb = self.model.encode(text, normalize_embeddings=True)
        return emb


class ModelStrategy(abc.ABC):
    @abc.abstractmethod
    def fit(self, X, y):
        raise NotImplementedError()

    @abc.abstractmethod
    def predict(self, X):
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self, path: Path):
        raise NotImplementedError()

    @abc.abstractmethod
    def load(self, path: Path):
        raise NotImplementedError()


class SklearnModelStrategy(ModelStrategy):
    def __init__(self, model):
        self.model = model

    def fit(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def save(self, path: Path):
        joblib.dump(self.model, path)

    def load(self, path: Path):
        self.model = joblib.load(path)
        return self


class XGBoostModelStrategy(ModelStrategy):
    def __init__(self, model):
        self.model = model

    def fit(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def save(self, path: Path):
        joblib.dump(self.model, path)

    def load(self, path: Path):
        self.model = joblib.load(path)
        return self


def embedding_factory(name: str, **kwargs) -> EmbeddingStrategy:
    name = (name or "spacy").lower()
    if name == "spacy":
        return SpacyEmbedding(kwargs.get("nlp"))
    if name in ("fasttext", "gensim", "gensim-fasttext"):
        return GensimFastTextEmbedding(kwargs.get("ft_model"), kwargs.get("vector_size", 300))
    if name in ("mpnet", "sentence-transformer", "sentence_transformers"):
        return SentenceTransformerEmbedding(kwargs.get("model"))
    raise ValueError(f"Unknown embedding strategy: {name}")


def model_factory(name: str, model_obj=None) -> ModelStrategy:
    name = (name or "sklearn").lower()
    if name in ("sklearn", "randomforest", "rf"):
        return SklearnModelStrategy(model_obj)
    if name in ("xgboost", "xgb"):
        return XGBoostModelStrategy(model_obj)
    raise ValueError(f"Unknown model strategy: {name}")


def create_embedding_strategy(name: str) -> EmbeddingStrategy:
    name = (name or "spacy").lower()
    if name == "spacy":
        import spacy
        nlp = spacy.load("en_core_web_md")
        return embedding_factory("spacy", nlp=nlp)
    if name in ("fasttext", "gensim", "gensim-fasttext"):
        import gensim.downloader as api
        ft = api.load("fasttext-wiki-news-subwords-300")
        return embedding_factory("fasttext", ft_model=ft, vector_size=300)
    if name in ("mpnet", "sentence-transformers", "sentence_transformer"):
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
        return embedding_factory("mpnet", model=model)
    raise ValueError(f"Unknown embedding strategy: {name}")


def get_default_model_path(base_path: Path, model_name: str, emb_name: str) -> Path:
    model_name = (model_name or "rf").lower()
    filename = f"{emb_name}_{model_name}.joblib"
    return base_path / "models" / filename


def create_ml_model_strategy(name: str) -> ModelStrategy:
    name = (name or "rf").lower()
    if name in ("rf", "randomforest"):
        from sklearn.ensemble import RandomForestRegressor
        base_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        return model_factory("sklearn", model_obj=base_model)
    if name in ("xgb", "xgboost"):
        from xgboost import XGBRegressor
        base_model = XGBRegressor(
            n_estimators=300,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            objective="reg:squarederror",
            random_state=42,
            n_jobs=-1,
        )
        return model_factory("xgboost", model_obj=base_model)
    raise ValueError(f"Unknown model strategy: {name}")
