import spacy
import contractions

nlp = spacy.load("en_core_web_sm")

def normalize_text(text: str) -> str:
    text = contractions.fix(text)
    return text

def split_sentences(text: str) -> list[str]:
    normalized = normalize_text(text)

    doc = nlp(normalized)

    return [
        sent.text.strip()
        for sent in doc.sents
    ]