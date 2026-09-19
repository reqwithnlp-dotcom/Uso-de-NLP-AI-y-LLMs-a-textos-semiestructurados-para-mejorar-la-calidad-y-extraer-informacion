import spacy

from types import SimpleNamespace

from analyzer.analysis_context import AnalysisContext
from extractors.verb_features_context_extractor import VerbFeaturesContextExtractor


nlp = spacy.load("en_core_web_md")


def test_should_extract_non_verb_token_with_auxiliary():

    doc = nlp(
        "The system had process all pending transactions."
    )

    sentence = SimpleNamespace(
        text=doc.text,
        doc=doc
    )

    context = AnalysisContext(
        sentence=sentence
    )

    VerbFeaturesContextExtractor.extract(context)

    process_features = next(
        features
        for features in context.verb_features
        if features.token.text == "process"
    )

    assert process_features.verb_tag == "NN"

    assert [
        auxiliary.text.lower()
        for auxiliary in process_features.auxiliaries
    ] == ["had"]